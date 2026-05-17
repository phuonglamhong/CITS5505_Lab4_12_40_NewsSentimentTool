<!-- This template displays the results of the sentiment analysis performed on the uploaded text. 
It shows a preview of the text and a summary of the sentiment analysis, including percentages for positive, neutral, and negative sentiments, as well as the overall sentiment. 
The design is clean and responsive, using Tailwind CSS for styling. -->
{% extends "base.html" %}
{% block title %}Sentiment Analysis Result{% endblock %}
{% block body_class %}min-h-screen bg-gradient-to-br from-blue-100 via-gray-100 to-white{% endblock %}

{% block content %}

<header
  class="px-8 py-6 flex justify-between items-center bg-white/80 backdrop-blur shadow-sm sticky top-0 z-10"
>
  <h1 class="text-xl font-bold text-blue-700">Sentiment Analysis Result</h1>

  <button onclick="window.location.href='{{ url_for('upload.upload') }}'"
    class="px-4 py-2 rounded-full bg-white/70 hover:bg-white font-semibold">
    Back to Upload
  </button>
</header>

<section class="max-w-4xl mx-auto px-6 py-12">

  <h2 class="text-3xl font-bold mb-6 text-center">Your Analysis</h2>

  <!-- Text Preview -->
  {% if session.text_content %}
  <div class="mb-8 bg-white p-6 rounded-xl shadow">
    <h3 class="text-xl font-semibold mb-2">Text Preview</h3>
    <p class="text-gray-700 whitespace-pre-line">{{ session.text_content }}</p>
  </div>
  {% endif %}

  <!-- Sentiment Result -->
  {% if session.sentiment_data %}
  <div class="bg-white p-6 rounded-xl shadow">
    <h3 class="text-xl font-semibold mb-4">Sentiment Summary</h3>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">

      <div class="p-4 rounded-lg bg-green-100 shadow">
        <p class="text-lg font-bold text-green-700">Positive</p>
        <p class="text-2xl font-semibold">{{ session.sentiment_data.positive_pct }}%</p>
      </div>

      <div class="p-4 rounded-lg bg-gray-200 shadow">
        <p class="text-lg font-bold text-gray-700">Neutral</p>
        <p class="text-2xl font-semibold">{{ session.sentiment_data.neutral_pct }}%</p>
      </div>

      <div class="p-4 rounded-lg bg-red-100 shadow">
        <p class="text-lg font-bold text-red-700">Negative</p>
        <p class="text-2xl font-semibold">{{ session.sentiment_data.negative_pct }}%</p>
      </div>

    </div>

    <!-- Overall sentiment -->
    <div class="mt-6 text-center">
      <p class="text-xl font-bold">
        Overall Sentiment:
        <span class="capitalize text-blue-700">{{ session.sentiment_data.details[0].sentiment }}</span>
      </p>
    </div>

  </div>
  {% else %}
  <p class="text-center text-gray-600">No sentiment data available.</p>
  {% endif %}

</section>

{% endblock %}
