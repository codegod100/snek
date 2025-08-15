<button id="{{ button_id }}" class="bg-[#a6e3a1] text-[#11111b] px-8 py-3 rounded-lg font-semibold hover:bg-[#94e2d5] transition-colors duration-200 active:scale-95 transform">
  {{ button_text }}
  {% if button_text %}
    <span class="ml-2">🚀</span>
  {% endif %}
</button>