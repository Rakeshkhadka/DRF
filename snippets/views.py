from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from rest_framework import renderers


@api_view(['GET', 'POST',])
@renderer_classes([renderers.JSONRenderer, renderers.BrowsableAPIRenderer])
def snippet_list(request, format=None):
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializers = SnippetSerializer(snippets, many=True)
        return Response(serializers.data)
    elif request.method == "POST":
        serializers = SnippetSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    snippet = get_object_or_404(Snippet, id=pk)

    if request.method == "GET":
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)