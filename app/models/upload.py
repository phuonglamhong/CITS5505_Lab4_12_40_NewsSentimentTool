<!-- This template provides a user interface for uploading text for sentiment analysis.
Users can paste their text into a textarea and submit it for analysis. -->
{% extends "base.html" %}
{% block title %}Upload & Search News{% endblock %}
{% block body_class %}min-h-screen bg-gradient-to-br from-blue-100 via-gray-100 to-white{% endblock %}

{% block content %}

<header
  class="px-8 py-6 flex justify-between items-center bg-white/80 backdrop-blur shadow-sm sticky top-0 z-10"
>
  <h1 class="text-xl font-bold text-blue-700">Upload & Search News</h1>

  <button onclick="window.location.href='{{ url_for('main.dashboard') }}'"
    class="px-4 py-2 rounded-full bg-white/70 hover:bg-white font-semibold">
    Back to Dashboard
  </button>
</header>

<section class="max-w-4xl mx-auto px-6 py-12">

  <!-- Tabs -->
  <div class="flex justify-center mb-8">
    <button id="tab-upload"
      class="px-6 py-2 rounded-l-full bg-blue-700 text-white font-semibold shadow">
      Manual Upload
    </button>
    <button id="tab-search"
      class="px-6 py-2 rounded-r-full bg-white text-gray-700 font-semibold shadow hover:bg-gray-100">
      Search Online News
    </button>
  </div>

  <!-- Manual Upload Section -->
  <div id="section-upload" class="bg-white p-6 rounded-xl shadow-lg">
    <h2 class="text-2xl font-bold mb-4">Paste Text for Analysis</h2>

    <form method="POST">
      <textarea name="content" rows="8"
        class="w-full p-4 rounded-lg shadow bg-gray-50"
        placeholder="Paste your text here..."></textarea>

      <button type="submit"
        class="mt-4 px-6 py-3 bg-blue-700 text-white rounded-full font-semibold shadow hover:-translate-y-1 transition">
        Analyze Text
      </button>
    </form>
  </div>
</script>

{% endblock %}
