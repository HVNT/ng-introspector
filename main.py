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


def print_recipes():
    for key, recipe in recipes.iteritems():
        for recipeItem in recipe:
            # if not already in unique add to unique
            if recipeItem not in uniqueRecipes[key]:
                uniqueRecipes[key].append(recipeItem)

    for key, uRecipe in uniqueRecipes.iteritems():
        print('\t- %s recipes (total: %s)' % (key, len(uRecipe)))


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
    js_file = open(file_path, 'r')
    for line in js_file:
        inspected_line = inspect_js_line(line)
        if inspected_line:
            namespace = parse_recipe_namespace(line, inspected_line)
            recipes[inspected_line].append(namespace)
            # print namespace


def traverse(dir_path, ignore_dirs):
    for root, subdirs, files in os.walk(dir_path):
        if can_traverse(root, ignore_dirs):
            # print('--\nroot = ' + root)

            # for subdir in subdirs:
            # print('\t- subdirectory ' + subdir)

            for filename in files:
                if filename.endswith('.js'):
                    jsMeta['fileCount'] += 1
                    file_path = os.path.join(root, filename)
                    inspect_js(file_path)
                    # print('\t- file %s' % filename)
                    # print('\t- file %s (full path: %s)' % (filename, file_path))

    print_recipes()
    print('-----\njs file count: %s' % jsMeta['fileCount'])


def main():
    dir_path = sys.argv[1]  # relative path to directory that contains ng project to be introspected
    ignore_dirs = sys.argv[2]
    ignore_dirs = ignore_dirs.split(',')
    traverse(dir_path, ignore_dirs)


if __name__ == "__main__":
    main()
