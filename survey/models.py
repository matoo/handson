from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list
from django.db import models


DIFFICULT_POINTS_CHOICES = (
  (0, '環境構築（Python、Djangoのインストール）'),
  (1, '環境構築（Djangoのセットアップ、プロジェクト作成）'),
  (2, '環境構築（Herokuのセットアップ、デプロイ）'),
  (3, '環境構築（Gitのセットアップ）'),
  (4, 'ログインページを作る'),
  (5, 'Django urls'),
  (6, 'Django views'),
  (7, 'HTMLテンプレート作成'),
  (8, 'データベース操作'),
  (9, 'CSSの設定'),
  (10, 'テンプレートの拡張'),
  (11, 'アプリケーションの拡張'),
  (12, 'フォームの作成'),
  (13, 'その他'),
)

choices = {}
choices['time_settings'] = (
  ('too long', '長すぎる'), ('long', '長い'), ('just right', 'ちょうど良い'), ('short', '短い'), ('too short', '短すぎる'),
)
choices['handson_level'] = (
  ('too difficult', '難しすぎる'), ('difficult', '難しい'), ('understand', '理解できた'), ('easy', '易しい'), ('too easy', '易しすぎる'),
)
choices['handson_interest'] = (
  ('overall', '全体的に知りたい内容を含んでいた'), ('some', '一部知りたい内容を含んでいた'), ('thin', '興味関心が薄い分野だった'),
)
choices['handson_quantity'] = (
  ('too many', '項目が多すぎる'), ('many', '項目が多い'), ('just right', 'ちょうど良い'), ('short', '項目が少ない'), ('too short', '項目が少なすぎる'),
)

class Questionnaire(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)
  how_about_handson = models.TextField(default='', blank=True)
  difficult_points = models.CharField(max_length=128, blank=True,
                                      validators=[validate_comma_separated_integer_list])
  difficult_other = models.TextField(default='', blank=True)
  time_settings = models.CharField(max_length=16, choices=choices['time_settings'])
  handson_level = models.CharField(max_length=16, choices=choices['handson_level'])
  handson_interest = models.CharField(max_length=8, choices=choices['handson_interest'])
  handson_quantity = models.CharField(max_length=16, choices=choices['handson_quantity'])
  free_opinions = models.TextField(default='', blank=True)
  interest_trainings = models.TextField(default='', blank=True)

  def __str__(self):
    return str(self.user)
