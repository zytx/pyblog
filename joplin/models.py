from django.db import models


class Folder(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    created_time = models.IntegerField()
    updated_time = models.IntegerField()
    user_created_time = models.IntegerField()
    user_updated_time = models.IntegerField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'folders'
        managed = False


class Tag(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    created_time = models.IntegerField()
    updated_time = models.IntegerField()
    user_created_time = models.IntegerField()
    user_updated_time = models.IntegerField()

    class Meta:
        db_table = 'tags'
        managed = False


class Resource(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    mime = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    created_time = models.IntegerField()
    updated_time = models.IntegerField()
    user_created_time = models.IntegerField()
    user_updated_time = models.IntegerField()
    file_extension = models.CharField(max_length=255)
    size = models.IntegerField()

    class Meta:
        db_table = 'resources'
        managed = False


class NoteTags(models.Model):
    note = models.ForeignKey('Note', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_time = models.IntegerField()
    updated_time = models.IntegerField()
    user_created_time = models.IntegerField()
    user_updated_time = models.IntegerField()

    class Meta:
        db_table = 'note_tags'
        managed = False


class NoteResources(models.Model):
    note = models.ForeignKey('Note', on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    is_associated = models.IntegerField()
    last_seen_time = models.IntegerField()

    class Meta:
        db_table = 'note_resources'
        managed = False


class Note(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    parent = models.ForeignKey('self', models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_conflict = models.IntegerField()
    source_url = models.CharField(max_length=255)
    is_todo = models.IntegerField()
    created_time = models.IntegerField()
    updated_time = models.IntegerField()
    user_created_time = models.IntegerField()
    user_updated_time = models.IntegerField()

    tags = models.ManyToManyField(Tag, through='NoteTags')
    resources = models.ManyToManyField(Resource, through='NoteResources')

    class Meta:
        db_table = 'notes'
        managed = False
