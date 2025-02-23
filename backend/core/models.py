from openai import OpenAI

from django.db import models

from core.tasks import handle_ai_request_job


class Recipe(models.Model):
    """Represents a recipe in the system."""
    name = models.CharField(max_length=255)
    steps = models.TextField()

    def __str__(self):
        return self.name


class AiChatSession(models.Model):
    """Tracks an AI chat session."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AiRequest(models.Model):
    """Represents an AI request."""

    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETE = 'complete'
    FAILED = 'failed'
    STATUS_OPTIONS = (
        (PENDING, 'Pending'),
        (RUNNING, 'Running'),
        (COMPLETE, 'Complete'),
        (FAILED, 'Failed')
    )

    status = models.CharField(choices=STATUS_OPTIONS, default=PENDING)
    session = models.ForeignKey(
        AiChatSession,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    messages = models.JSONField()
    response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _queue_job(self):
        """Add job to queue."""
        handle_ai_request_job.delay(self.id)

    def handle(self):
        """Handle request."""
        self.status = self.RUNNING
        self.save()
        client = OpenAI()
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages,
            )
            self.response = completion.to_dict()
            self.status = self.COMPLETE
        except Exception:
            self.status = self.FAILED

        self.save()

    def save(self, **kwargs):
        is_new = self._state.adding
        super().save(**kwargs)
        if is_new:
            self._queue_job()
