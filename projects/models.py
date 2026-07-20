from django.db import models


class SingletonModel(models.Model):
    """
    Base class for models that should only ever have one row (e.g. the
    Hero section, the About section header, site-wide settings).

    Call `YourModel.load()` to fetch the single instance, creating it
    with field defaults on first access.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # singleton rows are never deleted

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
    
class ProjectSection(SingletonModel):
    """
    Singleton-style section header for the Work/Projects area — same
    idea as the Skills section: eyebrow / heading / intro copy that
    sits above the list of individual project cards.
    """
    eyebrow = models.CharField(max_length=100, blank=True, default = 'Projects — 2026')
    heading = models.CharField(max_length=150, blank=True, default='Projects')
    intro = models.TextField(blank=True,default="A selection of projects I've built.")

    class Meta:
        verbose_name = "Projects section"
        verbose_name_plural = "Projects section"

    def __str__(self):
        return self.heading or "Projects section"


class Project(models.Model):
    section = models.ForeignKey(
        ProjectSection,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    title = models.CharField(max_length=150)
    year = models.CharField(max_length=10, blank=True)
    role = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    # comma-separated, matches the frontend's tagList() split-on-comma helper
    tags = models.CharField(max_length=300, blank=True)
    image = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    code_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title