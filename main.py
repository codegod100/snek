from pyscript import document
import re

counter = 0

class CustomTemplateEngine:
    def __init__(self):
        self.templates = {}
    
    def load_template(self, name, content):
        """Load a template from content"""
        self.templates[name] = content
    
    def load_from_file(self, name, filepath):
        """Load template from PyScript filesystem"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                self.load_template(name, content)
                return True
        except Exception as e:
            print(f"Failed to load template {name}: {e}")
            return False
    
    def render(self, template_name, **context):
        """Render template with context variables"""
        if template_name not in self.templates:
            return f"Template '{template_name}' not found"
        
        template = self.templates[template_name]
        
        # Replace {{variable}} with context values
        def replace_var(match):
            var_name = match.group(1).strip()
            return str(context.get(var_name, f"{{{{ {var_name} }}}}"))
        
        # Support {{variable}} syntax
        result = re.sub(r'\{\{\s*(\w+)\s*\}\}', replace_var, template)
        
        # Support {% if condition %} {% endif %} blocks
        def replace_if_block(match):
            condition = match.group(1).strip()
            content = match.group(2)
            
            # Simple condition evaluation
            if condition in context and context[condition]:
                return content
            return ""
        
        # Use manual multiline matching instead of re.DOTALL
        pattern = r'\{\%\s*if\s+(\w+)\s*\%\}([\s\S]*?)\{\%\s*endif\s*\%\}'
        result = re.sub(pattern, replace_if_block, result)
        
        return result

# Initialize template engine
template_engine = CustomTemplateEngine()

def load_templates():
    """Load templates from PyScript filesystem"""
    success = True
    success &= template_engine.load_from_file('counter', '/templates/counter.tpl')
    success &= template_engine.load_from_file('button', '/templates/button.tpl')
    
    if not success:
        # Fallback templates if file loading fails
        template_engine.load_template('counter', '''
<div class="text-6xl font-bold mb-8 text-[#89b4fa] bg-[#11111b] px-6 py-4 rounded-lg border border-[#45475a]">
  {{ count }}
</div>
        '''.strip())
        
        template_engine.load_template('button', '''
<button id="{{ button_id }}" class="bg-[#a6e3a1] text-[#11111b] px-8 py-3 rounded-lg font-semibold hover:bg-[#94e2d5] transition-colors duration-200 active:scale-95 transform">
  {{ button_text }}
</button>
        '''.strip())

def render_counter():
    return template_engine.render('counter', count=counter)

def render_button():
    return template_engine.render('button', 
                                button_id="increment-btn", 
                                button_text="Increment")

def increment_counter(event):
    global counter
    counter += 1
    document.getElementById("counter").innerHTML = render_counter()

def init_app():
    load_templates()
    document.getElementById("counter").innerHTML = render_counter()
    document.getElementById("increment-btn").outerHTML = render_button()
    document.getElementById("increment-btn").onclick = increment_counter

init_app()
