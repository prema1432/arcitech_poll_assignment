from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from poll.forms import PollForm, PollOptionForm
from poll.models import Poll, PollOption, Vote


# Create your views here.

def index(request):
    context = {}
    latest_polls = Poll.objects.all().order_by('-created_at')
    context['latest_polls'] = latest_polls
    return render(request, 'index.html', context)


@login_required
def create_poll(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        option_formset = modelformset_factory(PollOption, form=PollOptionForm, min_num=1, validate_min=True)(
            request.POST)
        if poll_form.is_valid() and option_formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            print("option_formset", option_formset.cleaned_data)
            option_instances = option_formset.save(commit=False)
            for option in option_instances:
                option.poll = poll
                option.save()
            return HttpResponseRedirect(reverse('polls:poll_detail', args=(poll.id,)))
    else:
        poll_form = PollForm()
        option_formset = modelformset_factory(PollOption, form=PollOptionForm, min_num=1, validate_min=True)(
            queryset=PollOption.objects.none())
    return render(request, 'polls/create_poll.html', {'poll_form': poll_form, 'option_formset': option_formset})


@login_required
def poll_detail(request, poll_id):
    context = {}
    poll = get_object_or_404(Poll, id=poll_id)
    user_has_voted = poll.options.filter(voted__voter=request.user).exists()
    options = poll.options.all()
    if request.method == 'POST':
        selected_option = request.POST['option']
        option = get_object_or_404(PollOption, id=selected_option)
        option.votes += 1
        option.save()
        vote = Vote(poll_option=option, voter=request.user)
        vote.save()
        return HttpResponseRedirect(reverse('polls:poll_results', args=(poll.id,)))
    return render(request, 'polls/poll_detail.html',
                  {'poll': poll, 'user_has_voted': user_has_voted, 'options': options})


@login_required
def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    options = poll.options.all()
    return render(request, 'polls/poll_results.html', {'poll': poll, 'options': options})
