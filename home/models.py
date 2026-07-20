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


# ---------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------

class HeroContent(SingletonModel):
    eyebrow = models.CharField(max_length=100, default="Portfolio — 2026")
    name = models.CharField(max_length=100, default="Prabin.O")
    role = models.CharField(max_length=150, default="Fullstack Developer & Designer")
    tagline = models.CharField(max_length=200, default="I build interfaces that feel alive.")
    description = models.TextField(blank=True)

    primary_cta_label = models.CharField(max_length=50, default="View the projects")
    secondary_cta_label = models.CharField(max_length=50, default="Download Cv")
   

    image = models.URLField(blank=True, help_text="Portrait shown in the hero frame.")
    image_alt = models.CharField(max_length=200, blank=True)

    

    class Meta:
        verbose_name = "Hero content"

    def __str__(self):
        return "Hero content"


# ---------------------------------------------------------------------
# About
# ---------------------------------------------------------------------

class AboutContent(SingletonModel):
    eyebrow = models.CharField(max_length=100, default="About — 2026")
    heading = models.CharField(max_length=150, default="A little about me")
    bio = models.TextField(blank=True)
    bio_secondary = models.TextField(blank=True)
    status = models.CharField(max_length=150, default="Available for new projects")

    class Meta:
        verbose_name = "About content"

    def __str__(self):
        return "About content"


class Stat(models.Model):
    """A single animated stat card on the About section (e.g. '24+ Projects completed')."""

    about = models.ForeignKey(AboutContent, related_name="stats", on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)
    suffix = models.CharField(max_length=10, blank=True, help_text="e.g. '+', '%'")
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value}{self.suffix} — {self.label}"


#messages

class Messages(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField( max_length=254)
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    