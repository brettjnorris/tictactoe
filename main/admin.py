from django.contrib import admin
from models import Game, Move

class MoveInline(admin.TabularInline):
  model = Move
  extra = 0

class GameAdmin(admin.ModelAdmin):
  inlines = [MoveInline]

admin.site.register(Game, GameAdmin)
admin.site.register(Move)
