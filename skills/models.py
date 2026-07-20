from django.db import models

# Create your models here.



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


class SkillsSection(SingletonModel):
    eyebrow = models.CharField(max_length=100, default="Toolkit — 2026")
    heading = models.CharField(max_length=150, default="Skills")
    intro = models.TextField(blank=True)

    class Meta:
        verbose_name = "Skills section content"

    def __str__(self):
        return "Skills section content"


class SkillGroup(models.Model):
    section = models.ForeignKey(SkillsSection, related_name="groups", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    note = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Skill(models.Model):
    class Level(models.TextChoices):
        PRIMARY = "primary", "Primary (featured tile)"
        SECONDARY = "secondary", "Secondary (compact chip)"

    group = models.ForeignKey(SkillGroup, related_name="skills", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="simple-icons slug, e.g. 'react', 'python', 'docker'.",
    )
    color = models.CharField(
        max_length=6,
        blank=True,
        default="F5F1EA",
        help_text="Hex color without the '#', e.g. 'F7DF1E'.",
    )
    level = models.CharField(max_length=10, choices=Level.choices, default=Level.SECONDARY)
    note = models.CharField(max_length=150, blank=True, help_text="Shown only for primary skills.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name
