---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title: coming soon
---

coming soon

{% for post in site.artist %}
- [{{ post.name }}]({{ post.url }})
{% endfor %}
