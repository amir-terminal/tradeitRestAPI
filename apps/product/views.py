from rest_framework.fields import SerializerMethodField
from .serializers import CategorySerializer, ProductSerializer
from django.http.response import JsonResponse
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import viewsets
# from rest_framework.serializers import ModelSerializer
# from rest_framework.decorators import action

# Create your views here.
from django.shortcuts import get_object_or_404, render
from .models import Category, Product
