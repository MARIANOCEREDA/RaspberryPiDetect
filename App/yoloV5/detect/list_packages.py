import pkgutil

def list_subpackages(package_name):
    package = __import__(package_name)
    subpackages = []
    
    for _, name, is_pkg in pkgutil.walk_packages(package.__path__, package_name + '.'):
        if is_pkg:
            subpackages.append(name)
    
    return subpackages

package_name = 'yoloV5'
subpackages = list_subpackages(package_name)
print("Subpackages of", package_name, ":", subpackages)