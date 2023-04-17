from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Poll(TimeStampedModel):
    question = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls_created')

    def __str__(self):
        return self.question

    def total_votes(self):
        total = 0
        for option in self.options.all():
            total += option.votes
        return total


class PollOption(TimeStampedModel):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.option

    @property
    def get_voting_percentage(self):
        total_votes = self.poll.total_votes()
        if total_votes == 0:
            return 0
        voting_percentage = (self.votes / total_votes) * 100
        return round(voting_percentage, 2)


class Vote(TimeStampedModel):
    poll_option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='voted')
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.voter.username} voted for {self.poll_option.option}'
