from django.db import models

# Create your models here.

#init data for models:
# https://docs.djangoproject.com/en/2.2/howto/initial-data/

# level 1
class user_type(models.Model):
    """
    Тип пользователя: Тренер, Спортсмен
    """
    USER_TYPES = (
        ('Tr', 'Тренер'),
        ('Sp', 'Спортсмен')
    )
    user_type = models.CharField(max_length=2, choices=USER_TYPES)

    def __str__(self):
        return self.get_user_type_display()

class classification(models.Model):
    """
    Звание: Мастер спорта международного класса, первый разряд, заслуженный тренер России, ...
    """
    classification = models.CharField(max_length=18)

    def __str__(self):
        return self.classification

class sport_discipline(models.Model):
    """-
    Cпортивная дисциплина. Пример из домена наиболее длинного названия спортивной дисциплины: "Лыжное
двоеборье на Олимпийских играх"
    """
    sport_discipline = models.CharField(max_length=37)
    
    def __str__(self):
        return self.sport_discipline

    
class role_in_team(models.Model):
    """
    Роль в команде. тренер, помощник тренера, игрок, участник, судья.
    """
    TEAM_ROLES = (
        ('Tr', 'Тренер'),
        ('TH', 'Помощник тренера'),
        ('Pl', 'Игрок'),
        ('Pa', 'Участник'),
        ('Ju', 'Судья'),
    )
    role_in_team = models.CharField(max_length=2, choices=TEAM_ROLES)

    def __str__(self):
        return self.get_role_in_team_display()



# level 2
class user(models.Model):
    """
    Пользователь
    """
    # https://stackoverflow.com/questions/2475249/what-are-the-options-for-overriding-djangos-cascading-delete-behaviour
    user_type = models.ForeignKey(user_type, null=True, on_delete=models.SET_NULL)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=140)
    patronic_name = models.CharField(max_length=30, blank=True)
    document_number = models.IntegerField()


class team(models.Model):
    """
    Команда
    """
    creator = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)

class training(models.Model):
    """
    Тренировка
    """
    creator = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(team, null=True, on_delete=models.SET_NULL)
    date_begin = models.DateField()
    date_end = models.DateField()
    place_address = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=13, decimal_places=2)

class competition(models.Model):
    """
    Соревнование
    """
    creator = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    date_begin = models.DateField()
    date_end = models.DateField()
    place_address = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    prize_fund = models.DecimalField(max_digits=13, decimal_places=2)


class user_qualification(models.Model):
    """
    Квалификация пользователя
    """
    user = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    classification = models.ForeignKey(classification, null=True, on_delete=models.SET_NULL)
    sport_discipline = models.ForeignKey(sport_discipline, null=True, on_delete=models.SET_NULL)
    date = models.DateField()
    expiration_date = models.DateField()


# level 3
class team_competition(models.Model):
    """
    Регистрация команды team на соревнование competition
    """
    competition = models.ForeignKey(competition, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(team, null=True, on_delete=models.SET_NULL)
    registration_date = models.DateField()


class user_training(models.Model):
    """
    Регистрация пользователя user на тренировку training
    """
    training = models.ForeignKey(training, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    registration_date = models.DateField()
    
class user_competition(models.Model):
    """
    Индивидуальное участие пользователя user в соревновании competition
    """
    competition = models.ForeignKey(competition, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    registration_date = models.DateField()

    
class user_team(models.Model):
    """
    Членство пользователя user в роли role в команде team
    """
    user = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    role = models.ForeignKey(role_in_team, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(team, null=True, on_delete=models.SET_NULL)