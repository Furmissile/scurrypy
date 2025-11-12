import importlib
import scurrypy

for name, module_path in scurrypy._mapping.items():
    try:
        module = importlib.import_module(module_path)
        getattr(module, name)
    except ModuleNotFoundError as e:
        print(f"⚠️ Module not found for {name}: {module_path}")
    except AttributeError as e:
        print(f"❌ {module_path} has no attribute {name}")
    else:
        print(f"✅ {module_path}.{name}")
