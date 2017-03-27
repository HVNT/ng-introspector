import string
import sys
import os

jsMeta = {
    'lineCount': 0,
    'fileCount': 0
}

recipe_rules = {
    'modules': 'angular.module(\'',
    'controllers': '.controller(\'',
    'services': '.service(\'',
    'factories': '.factory(\'',
    'directives': '.directive(\'',
    'filters': '.filter(\'',
    'animations': '.animation(\'',
    'providers': '.provider(\''
}

recipes = {
    'modules': [],
    'controllers': [],
    'services': [],
    'factories': [],
    'directives': [],
    'filters': [],
    'animations': [],
    'providers': []
}

uniqueRecipes = {
    'modules': [],
    'controllers': [],
    'services': [],
    'factories': [],
    'directives': [],
    'filters': [],
    'animations': [],
    'providers': []
}

modules = {}
uniqueModules = {}


def init_module(namespace):
    modules[namespace] = {
        'controllers': [],
        'services': [],
        'factories': [],
        'directives': [],
        'filters': [],
        'animations': [],
        'providers': []
    }

    uniqueModules[namespace] = {
        'controllers': [],
        'services': [],
        'factories': [],
        'directives': [],
        'filters': [],
        'animations': [],
        'providers': []
    }


def can_traverse(path, ignore_dirs):
    for ignore_dir in ignore_dirs:
        if ignore_dir in path:
            return False
    return True


def parse_recipe_namespace(line, rule_key):
    # hacky .. rewrite to use params rule_key lol
    tokens = line.split('(')
    tokens = tokens[1]
    tokens = tokens.split('\'')
    return tokens[1]


# returns recipe key if line. if none returns false
def inspect_js_line(line):
    for ruleKey, ruleValue in recipe_rules.iteritems():
        if ruleValue in line:
            return ruleKey
    return False


def inspect_js(file_path):
    current_module = None
    js_file = open(file_path, 'r')

    for line in js_file:
        jsMeta['lineCount'] += 1
        recipe_type = inspect_js_line(line)

        if recipe_type:
            recipe_namespace = parse_recipe_namespace(line, recipe_type)

            # init if needed
            if recipe_type is 'modules':
                module_namespace = recipe_namespace.split('.')
                module_namespace = module_namespace[0] + '.' + module_namespace[1]

                if module_namespace not in modules:
                    init_module(module_namespace)
                current_module = modules[module_namespace]  # set current module - that we will roll on to

            # roll onto global recipes
            recipes[recipe_type].append(recipe_namespace)

            if recipe_type is not 'modules' and current_module:
                current_module[recipe_type].append(recipe_namespace)  # append to global modules


def traverse(dir_path, ignore_dirs):
    for root, subdirs, files in os.walk(dir_path):
        if can_traverse(root, ignore_dirs):
            # print('--\nroot = ' + root)

            # for subdir in subdirs:
            #   print('\t- subdirectory ' + subdir)

            for filename in files:
                if filename.endswith('.js'):
                    jsMeta['fileCount'] += 1
                    file_path = os.path.join(root, filename)
                    inspect_js(file_path)
                    # print('\t- file %s (full path: %s)' % (filename, file_path))

    print('\n\tHERE IS YOUR INTROSPECTION\n')
    print_recipes()
    print_modules()
    print('\n\tNumber of JavaScript files \t%s' % jsMeta['fileCount'])
    print('\tLines of JavaScript \t\t%s' % jsMeta['lineCount'])
    print('\n')


def print_recipes():
    for key, recipe in recipes.iteritems():
        for recipeItem in recipe:
            # if not already in unique add to unique
            if recipeItem not in uniqueRecipes[key]:
                uniqueRecipes[key].append(recipeItem)

    for key, uRecipe in uniqueRecipes.iteritems():
        print('\t+ %s recipes \ttotal count: %s' % (key, len(uRecipe)))


def print_modules():
    for key, module in modules.iteritems():
        for recipeType, recipeValues in module.iteritems():
            for recipeValue in recipeValues:
                if recipeValue not in uniqueModules[key][recipeType]:
                    uniqueModules[key][recipeType].append(recipeValue)

    for key, uModule in uniqueModules.iteritems():
        print('\n\t %s' % key)
        for recipeType, recipeValues in uModule.iteritems():
            print('\t\t> %s \tcount: %s' % (recipeType, len(recipeValues)))


def main():
    dir_path = sys.argv[1]  # relative path to directory that contains ng project to be introspected
    ignore_dirs = sys.argv[2]
    ignore_dirs = ignore_dirs.split(',')
    traverse(dir_path, ignore_dirs)


if __name__ == "__main__":
    main()
