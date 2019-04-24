# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accountsinformation(models.Model):
    idaccount = models.AutoField(db_column='idAccount', primary_key=True)  # Field name made lowercase.
    idperson = models.IntegerField(db_column='IdPerson', blank=True, null=True)  # Field name made lowercase.
    media = models.CharField(db_column='Media', max_length=16, blank=True, null=True)  # Field name made lowercase.
    headportrait = models.CharField(db_column='HeadPortrait', max_length=45, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True)  # Field name made lowercase.
    follownumber = models.IntegerField(db_column='FollowNumber', blank=True, null=True)  # Field name made lowercase.
    fansnumber = models.IntegerField(db_column='FansNumber', blank=True, null=True)  # Field name made lowercase.
    tweetsnumber = models.IntegerField(db_column='TweetsNumber', blank=True, null=True)  # Field name made lowercase.
    lasttweettime = models.DateField(db_column='LastTweetTime', blank=True, null=True)  # Field name made lowercase.
    userlocation = models.CharField(db_column='UserLocation', max_length=16, blank=True, null=True)  # Field name made lowercase.
    severity = models.DecimalField(db_column='Severity', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = u"账号信息"
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'accountsinformation'

    def __str__(self):
        return self.username


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Friendcircle(models.Model):
    media = models.CharField(db_column='media', max_length=255, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='name', max_length=255, null=True)  # Field name made lowercase.
    to_name = models.CharField(db_column='to_name', max_length=255)  # Field name made lowercase.
    relation = models.CharField(db_column='relation', max_length=255)  # Field name made lowercase.

    class Meta:
        verbose_name = u"朋友圈"
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'friend_circle'

    def __str__(self):
        return self.name


class Lifetimelist(models.Model):
    personnumber = models.IntegerField(db_column='PersonNumber', blank=True, null=True)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    introduction = models.CharField(db_column='Introduction', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lifetimelist'


class LogIn(models.Model):
    iduser = models.AutoField(db_column='IdUser', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'log_in'


class Personevent(models.Model):
    # id_label = models.AutoField(db_column='id_label', primary_key=True)  # Field name made lowercase.
    person = models.CharField(db_column='person', max_length=45)
    event = models.CharField(db_column='event', max_length=45)

    class Meta:
        managed = False
        db_table = 'person_event'


class Personlabel(models.Model):
    id_label = models.AutoField(db_column='id_label', primary_key=True)  # Field name made lowercase.
    id_person = models.IntegerField(db_column='id_person')
    label = models.CharField(db_column='label', max_length=45)

    class Meta:
        managed = False
        db_table = 'person_label'


class Sensitiveevent(models.Model):
    sensitivevent = models.CharField(db_column='SensitivEvent', max_length=45, blank=True, null=True)  # Field name made lowercase.
    idsensitivevent = models.IntegerField(db_column='IdSensitivEvent', primary_key=True)  # Field name made lowercase.
    tweetsnum = models.IntegerField(db_column='TweetsNum', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='content', blank=True)  # Field name made lowercase.
    sensitivity = models.DecimalField(db_column='Sensitivity', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    hot = models.DecimalField(db_column='Hot', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    respondnumber = models.IntegerField(db_column='RespondNumber', blank=True, null=True)  # Field name made lowercase.
    commentnumber = models.IntegerField(db_column='CommentNumber', blank=True, null=True)  # Field name made lowercase.
    sensitivewords = models.CharField(db_column='SensitiveWords', max_length=45, blank=True, null=True)  # Field name made lowercase.
    warning = models.DecimalField(db_column='Warning', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    label = models.CharField(db_column='label', max_length=45)

    class Meta:
        managed = False
        db_table = 'sensitiveevent'


class Similarpeople(models.Model):
    label = models.CharField(db_column='label', max_length=45)
    similar_person = models.CharField(db_column='similar_person', max_length=45, null=True)
    similarity = models.IntegerField(db_column='similarity', null=True)
    id_person = models.IntegerField(db_column='id_person', null=True)

    class Meta:
        managed = False
        db_table = 'similar_people'


class Supversiedpersonlist(models.Model):
    idperson = models.IntegerField(db_column='IdPerson', primary_key=True)  # Field name made lowercase.
    photo = models.CharField(db_column='photo', max_length=45, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=16)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=2, blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    tweetsnumber = models.IntegerField(db_column='TweetsNumber', blank=True, null=True)  # Field name made lowercase.
    userlocation = models.CharField(db_column='UserLocation', max_length=16, blank=True, null=True)  # Field name made lowercase.
    lasttweetstime = models.DateField(db_column='LastTweetsTime', blank=True, null=True)  # Field name made lowercase.
    hot = models.IntegerField(blank=True, null=True)
    introduction = models.TextField(db_column='Introduction', blank=True)  # Field name made lowercase.

    class Meta:
        verbose_name = u"监控用户"
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'supversiedpersonlist'

    def __str__(self):
        return self.name


class Twieetslists(models.Model):
    idtweets = models.IntegerField(db_column='IdTweets', primary_key=True)  # Field name made lowercase.
    idperson = models.IntegerField(db_column='IdPerson', blank=True, null=True)  # Field name made lowercase.
    mediasource = models.CharField(db_column='MediaSource', max_length=16, blank=True, null=True)  # Field name made lowercase.
    tweets = models.CharField(db_column='Tweets', max_length=45, blank=True, null=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='keyWords', max_length=45, blank=True, null=True)  # Field name made lowercase.
    useraccounts = models.CharField(db_column='UserAccounts', max_length=45, blank=True, null=True)  # Field name made lowercase.
    transpond = models.IntegerField(db_column='Transpond', blank=True, null=True)  # Field name made lowercase.
    likes = models.IntegerField(db_column='Likes', blank=True, null=True)  # Field name made lowercase.
    comments = models.IntegerField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    origin = models.CharField(db_column='Origin', max_length=16, blank=True, null=True)  # Field name made lowercase.
    contextrange = models.CharField(db_column='ContextRange', max_length=16, blank=True, null=True)  # Field name made lowercase.
    tweetsdetails = models.TextField(db_column='TweetsDetails', blank=True, null=True)  # Field name made lowercase.
    idsensitivevent = models.IntegerField(db_column='IdSensitivevent', blank=True, null=True)  # Field name made lowercase.
    warning = models.IntegerField(db_column='Warning', blank=True, null=True)  # Field name made lowercase.
    label = models.CharField(db_column='label', max_length=45)

    class Meta:
        verbose_name = u"推文列表"
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'twieetslists'

    def __str__(self):
        return self.tweets


class Usersensitivewords(models.Model):
    sensitivevent = models.CharField(max_length=45)
    user = models.CharField(max_length=45)
    words = models.CharField(max_length=255)
    idwords = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'usersensitivewords'


class Wordstopic(models.Model):
    idperson = models.IntegerField(db_column='IdPerson', blank=True, null=True)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    userspeech = models.CharField(db_column='UserSpeech', max_length=45, blank=True, null=True)  # Field name made lowercase.
    speechsource = models.CharField(db_column='SpeechSource', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wordstopic'
