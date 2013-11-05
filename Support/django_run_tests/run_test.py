#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by Uğur Özyılmazel on 2012-08-20.
Copyright (c) 2012 Fontronik. All rights reserved.
"""
import sys
import os
import re
import subprocess
import shlex
import cgi


TM_FILEPATH          = os.environ['TM_FILEPATH']
TM_FILENAME          = os.environ['TM_FILENAME']
TM_DIRECTORY         = os.environ['TM_DIRECTORY']
TM_PROJECT_DIRECTORY = os.environ['TM_PROJECT_DIRECTORY']
TM_BUNDLE_SUPPORT    = os.environ['TM_BUNDLE_SUPPORT']
HTML_BUNDLE          = "%s/django_run_tests/html" % TM_BUNDLE_SUPPORT
APP                  = os.path.basename(TM_DIRECTORY)
DEFAULT_SETTINGS     = ""

ERROR_MESSAGES = {
    'APP_NAME': """
Please provide application name for test.
Put a python comment in to source like:
<code># APP = myapp</code>
""",
    'VIRTUAL_ENV': """
<p>You need to activate Virtual Environment<p>
<ol>
    <li>Close TextMate and Terminal</li>
    <li>Open Terminal and Activate VirtualEnv via: <code>workon ENV_NAME</code></li>
    <li> Now open project via: <code>mate .</code></li>
</ol>
""",
    'CLASSES_METHODS_NOT_FOUND': """
<p>Coudn't find and class / methods in this: <code>%s</code> file</p>
""",
    'HASH_APP_NOT_FOUND': """
<p>Please add hash / comment like:</p>
<pre># APP = name_of_your_app</pre>
<p>to continue testing...</p>
"""
}


def read_file(input):
    """read given file and return content."""
    f = open(input, 'r')
    data = f.read()
    f.close()
    return data


def show_tm_variables():
    """docstring for show_tm_variables"""
    out = ['<pre>']
    for key in sorted(os.environ.iterkeys()):
        if key.startswith('TM_'):
            spacer = (25 - len(key)) * " "
            out.append("%s:%s%s" % (key, spacer, os.environ[key]))
    out.append('</pre>')
    return "\n".join(out)


def print_html(title="Running Tests", html=None):
    """docstring for print_html"""
    html_file = read_file("%s/template.html" % HTML_BUNDLE)
    print html_file % {
        'PAGE_TITLE': title,
        'PAGE_CSS': "%s/styles.css" % HTML_BUNDLE,
        'HTML_INPUT': html
    }


def tag(tag, input, html_class=None, html_id=None, inline_style=None):
    """docstring for tag"""
    html_class_val = ""
    html_id_val = ""
    inline_style_val = ""
    if html_class: 
        html_class_val = ' class="%s"' % html_class
    if html_id:
        html_id_val = ' id="%s"' % html_id
    if inline_style:
        inline_style_val = ' style="%s"' % inline_style
    output = '<%(tag)s%(class)s%(id)s%(inline_css)s>%(input)s</%(tag)s>' % {
        'tag': tag,
        'input': input,
        'class': html_class_val,
        'id': html_id_val,
        'inline_css': inline_style_val,
    }
    return output


def error_print(title="Warning", text=None):
    """docstring for error_print"""
    html_title = tag('h4', title, html_class="alert-heading")
    html_body = "%s%s" % (html_title, text)
    return tag('div', html_body, html_class="alert alert-block")



def run_shell_command(command):
    """docstring for run_shell_command"""
    cmd = subprocess.Popen(shlex.split(command),
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = cmd.communicate()
    return cgi.escape("".join(result))


def main():
    """docstring for main"""
    output = []
    if not os.environ.has_key("VIRTUAL_ENV"):
        print_html(html=error_print(text=ERROR_MESSAGES['VIRTUAL_ENV']))
        return 0
    
    PYTHON = "%s/bin/python" % os.environ['VIRTUAL_ENV']
    
    # output.append('<pre>')
    # output.append("TM_FILEPATH: %s" % TM_FILEPATH)
    # output.append("TM_FILENAME: %s" % TM_FILENAME)
    # output.append("TM_DIRECTORY: %s" % TM_DIRECTORY)
    # output.append("TM_PROJECT_DIRECTORY: %s" % TM_PROJECT_DIRECTORY)
    # output.append("APP: %s" % APP)
    # output.append("PYTHON: %s" % PYTHON)
    # output.append('</pre>')
    # output.append(show_tm_variables())
    
    DATA = read_file(TM_FILEPATH)
    
    settings_file = re.search(r"[^#] *?SETTINGS = ([\w.]+)", DATA)
    if settings_file:
        DEFAULT_SETTINGS = " --settings=%s" % settings_file.groups()[0]
    hash_test = re.findall(r"[^#]# *?TEST = ([\w.]+)", DATA)
    
    if TM_FILENAME == 'models.py':
        output.append(tag('h1', "Running Tests for Model"))
        models = re.findall(r"class (.+)\(models.Model\):", DATA)
        
        if len(models) == 0:
            print_html(html=error_print(
                text=ERROR_MESSAGES['CLASSES_METHODS_NOT_FOUND'] % TM_FILENAME)
            )
            return 0
        shell_cmd = "%(python)s %(manage_py)s/manage.py test %(app)s.%(model)s --noinput %(settings)s"
        
        RUN_INDIVIDUAL_MODELS = False
        if len(hash_test) > 0:
            RUN_INDIVIDUAL_MODELS = True
        
        test_cmds = []
        if RUN_INDIVIDUAL_MODELS:
            output.append(tag('h2', "Individual Test(s)... %s" % len(hash_test)))
            for model in hash_test:
                test_cmds.append(shell_cmd % {
                    'python': PYTHON,
                    'manage_py': TM_PROJECT_DIRECTORY,
                    'app': APP,
                    'model': model,
                    'settings': DEFAULT_SETTINGS,
                })
        else:
            output.append(tag('h2', "Model Test(s)... %s" % len(models)))
            for model in models:
                output.append(tag('h4', "<small>%s</small>.%s" % (APP, model)))
            test_cmds = ["%(python)s %(manage_py)s/manage.py test %(app)s %(settings)s" % {
                'python': PYTHON,
                'manage_py': TM_PROJECT_DIRECTORY,
                'app': APP,
                'settings': DEFAULT_SETTINGS,
            }]
        for test in test_cmds:
            output.append(tag('h5', '%s' % test, html_class="code"))
            output.append(tag('pre', run_shell_command(test)))
            output.append('<br/><br/>')
        
    else:
        output.append(tag('h1', "Running Test Cases..."))

        RUN_INDIVIDUAL_TESTS = False

        hash_app_name = re.findall(r"# *?APP = (\w+)", DATA)
        ref = re.compile(r"^class (.+)\(.*?TestCase\):|^ +def (test_.+)\(self\):", re.MULTILINE)
        classes_and_methods = re.findall(ref, DATA)
        # print classes_and_methods
        if len(hash_app_name) == 0:
            print_html(html=error_print(
                text=ERROR_MESSAGES['HASH_APP_NOT_FOUND'])
            )
            return 0

        if len(hash_test) > 0:
            RUN_INDIVIDUAL_TESTS = True

        application_name = hash_app_name[-1:][0]
        shell_cmd = "%(python)s %(manage_py)s/manage.py test %(app)s.%(test)s --noinput %(settings)s"
        if RUN_INDIVIDUAL_TESTS:
            output.append(tag('h2', "Individual Tests... %s" % len(hash_test)))
            for testcase in hash_test:
                run_test = shell_cmd % {
                    'python': PYTHON,
                    'manage_py': TM_PROJECT_DIRECTORY,
                    'app': application_name,
                    'test': testcase,
                    'settings': DEFAULT_SETTINGS,
                }
                output.append(tag('h5', '%s.%s' % (application_name, testcase), html_class="code"))
                output.append(tag('pre', run_shell_command(run_test)))
                output.append('<br/><br/>')
            
        else:
            if len(classes_and_methods) == 0:
                print_html(html=error_print(
                    text=ERROR_MESSAGES['CLASSES_METHODS_NOT_FOUND'] % TM_FILENAME)
                )
                return 0
            output.append(tag('h2', "All Tests..."))
            to_test = []
            last_processed_class_name = ""
            class_name = ""
            j = -1
            for i in range(len(classes_and_methods)):
                if len(classes_and_methods[i][0]) > 0:
                    class_name = classes_and_methods[i][0]
                    to_test.append([class_name, []])
                    j = j + 1
                    last_processed_class_name = class_name
                else:
                    if class_name == last_processed_class_name:
                        to_test[j][1].append(classes_and_methods[i][1])
            
            if len(to_test) == 0:
                print_html(html=error_print(
                    text="<code>to_test</code> list returned empty"))
                return 0
            
            for item in to_test:
                class_name = item[0]
                for method_name in item[1]:
                    testcase = "%s.%s" % (class_name, method_name)
                    run_test = shell_cmd % {
                        'python': PYTHON,
                        'manage_py': TM_PROJECT_DIRECTORY,
                        'app': application_name,
                        'test': testcase,
                        'settings': DEFAULT_SETTINGS,
                    }
                    output.append(tag('h5', '%s.%s' % (application_name, testcase), html_class="code"))
                    output.append(tag('pre', run_shell_command(run_test)))

    print_html(html="\n".join(output))



if __name__ == "__main__":
    sys.exit(main())
