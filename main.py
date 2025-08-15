from pyscript import document
import re

counter = 0

class CustomTemplateEngine:
    def __init__(self):
        self.templates = {}
        self.compiled_templates = {}
        self.render_cache = {}
    
    def load_template(self, name, content):
        """Load a template from content"""
        self.templates[name] = content
        self._compile_template(name, content)
    
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
    
    def _compile_template(self, name, template):
        """Pre-compile template patterns for faster rendering"""
        # Pre-compile variable patterns
        var_pattern = re.compile(r'\{\{\s*(\w+)\s*\}\}')
        if_pattern = re.compile(r'\{\%\s*if\s+(\w+)\s*\%\}([\s\S]*?)\{\%\s*endif\s*\%\}')
        
        self.compiled_templates[name] = {
            'template': template,
            'var_pattern': var_pattern,
            'if_pattern': if_pattern
        }
    
    def render(self, template_name, **context):
        """Render template with context variables using cached compilation"""
        if template_name not in self.compiled_templates:
            return f"Template '{template_name}' not found"
        
        # Create cache key based on template and context
        cache_key = (template_name, tuple(sorted(context.items())))
        if cache_key in self.render_cache:
            return self.render_cache[cache_key]
        
        compiled = self.compiled_templates[template_name]
        template = compiled['template']
        
        # Replace {{variable}} with context values using pre-compiled pattern
        def replace_var(match):
            var_name = match.group(1).strip()
            return str(context.get(var_name, f"{{{{ {var_name} }}}}"))
        
        result = compiled['var_pattern'].sub(replace_var, template)
        
        # Support {% if condition %} {% endif %} blocks using pre-compiled pattern
        def replace_if_block(match):
            condition = match.group(1).strip()
            content = match.group(2)
            
            # Simple condition evaluation
            if condition in context and context[condition]:
                return content
            return ""
        
        result = compiled['if_pattern'].sub(replace_if_block, result)
        
        # Cache the result for future use
        self.render_cache[cache_key] = result
        return result
    
    def clear_cache(self):
        """Clear render cache"""
        self.render_cache.clear()

# Initialize template engine
template_engine = CustomTemplateEngine()

def load_templates():
    """Load and pre-compile templates from PyScript filesystem"""
    print("Loading templates...")
    template_engine.load_from_file('counter', '/templates/counter.tpl')
    template_engine.load_from_file('button', '/templates/button.tpl')
    
    # Pre-render common template combinations to warm cache
    print("Warming template cache...")
    template_engine.render('counter', count=0)
    template_engine.render('button', button_id="increment-btn", button_text="Increment")
    print("Templates ready!")

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
    
    # Hide loading and show app
    document.getElementById("loading").style.display = "none"
    document.getElementById("app").classList.remove("hidden")
    
    # Initialize app content
    document.getElementById("counter").innerHTML = render_counter()
    document.getElementById("increment-btn").outerHTML = render_button()
    document.getElementById("increment-btn").onclick = increment_counter

init_app()
