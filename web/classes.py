import core.data as data
import random
from core.web import app, discord, jinja_env
from web.application import requires_accepted
from flask import render_template, abort, request, url_for, redirect
from flask_discord import requires_authorization
from functools import wraps

department_list = {
    'TWOW Design': {
        'name': 'TWOW Design'
    },
    'Sociology': {
        'name': 'Sociology'
    },
    'Cultural Studies': {
        'name': 'Cultural Studies'
    },
    'Visual Arts': {
        'name': 'Visual Arts'
    },
    'Mathematics': {
        'name': 'Mathematics'
    }
}

professor_list = {
    '212983348325384200': {
        'id': '212983348325384200',
        'name': 'Prof. Biscuit'
    },
    '210285266814894081': {
        'id': '210285266814894081',
        'name': 'Sidney Chou XIII'
    },
    '212805953630896128': {
        'id': '212805953630896128',
        'name': 'Dr. Azurite'
    },
    '184768535107469314': {
        'id': '184768535107469314',
        'name': 'Dr. Dark'
    },
    '450096592582737920': {
        'id': '450096592582737920',
        'name': 'Dr. H'
    },
    '236257776421175296': {
        'id': '236257776421175296',
        'name': 'Dr. LB'
    },
    '849279934987894805': {
        'id': '849279934987894805',
        'name': 'Mr. E'
    }
}

class_list = {
    'BS003': {
        'id': 'BS003',
        'title': 'The Bachelor\'s of Art of Bachelor\'s of Science',
        'department': department_list['TWOW Design']['name'],
        'professor': professor_list['212983348325384200']['id'],
        'professor_name': professor_list['212983348325384200']['name'],
        'ta': professor_list['210285266814894081']['id'],
        'description': 'NOTE TO SELF: Replace this with some pretentious, academic-sounding explantion of just fucking winging it on the fly. I\'d say I couldn\'t believe that the dean\'s letting me get away with this, but I guess that\'s what a tenure\'s for.'
    },
    'COLL101': {
        'id': 'COLL101',
        'title': 'Intro to Collaborative Efforts',
        'department': department_list['Sociology']['name'],
        'professor': professor_list['212805953630896128']['id'],
        'professor_name': professor_list['212805953630896128']['name'],
        'ta': professor_list['236257776421175296']['id'],
        'description': 'Let\'s all hold hands (or bump elbows, haha) and get along! This class helps us have epic gamer friendships and develop bonds in a place befuddled by those dang computers.'
    },
    'WLAN101': {
        'id': 'WLAN101',
        'title': 'World Language TWOWing',
        'department': department_list['Cultural Studies']['name'],
        'professor': professor_list['184768535107469314']['id'],
        'professor_name': professor_list['184768535107469314']['name'],
        'ta': professor_list['450096592582737920']['id'],
        'description': 'A practical and culture-oriented class on TWOWing in another language - useful for whenever the English speaking world gets inevitably and brutally taken over by a non-specific Romance-language-speaking foreign power!'
    },
    'ART110': {
        'id': 'ART110',
        'title': 'Handwriting',
        'department': department_list['Visual Arts']['name'],
        'professor': professor_list['184768535107469314']['id'],
        'professor_name': professor_list['184768535107469314']['name'],
        'ta': None,
        'description': 'A practical and culture-oriented class on TWOWing in manual handwriting - useful for whenever all computers get strategically destroyed by a non-specific despotic anti-information authoritarian regime led by a Romance-language-speaking foreign power!'
    },
    'MATH210': {
        'id': 'MATH210',
        'title': 'Calculus III',
        'department': department_list['Mathematics']['name'],
        'professor': professor_list['450096592582737920']['id'],
        'professor_name': professor_list['450096592582737920']['name'],
        'ta': None,
        'description': 'Here you\'ll learn about differentiation and integration in multiple dimensions!'
    },
    'HIST314': {
        'id': 'HIST314',
        'title': 'TWOW History',
        'department': department_list['Cultural Studies']['name'],
        'professor': professor_list['212983348325384200']['id'],
        'professor_name': professor_list['212983348325384200']['name'],
        'ta': professor_list['210285266814894081']['id'],
        'description': '"An interdisciplinary overview of the greater historical trends over the past five years. Examination of important figures and innovations through cultural, mathematical, and interpersonal lenses."<br><br>"...did you get all that? Yeah, alright. I don\'t get why I\'m teaching this course if I\'m around for half of the curriculum. This is fucking stupid."'
    },
    'MATH141': {
        'id': 'MATH141',
        'title': 'Statistics and Modeling',
        'department': department_list['Mathematics']['name'],
        'professor': professor_list['236257776421175296']['id'],
        'professor_name': professor_list['236257776421175296']['name'],
        'ta': None,
        'description': 'Basic survey of statistics modeling techniques such as Gaussian distributions and inter-TWOW ranking systems and their applications. Qualitative analysis of strengths and weaknesses of various models.'
    },
    'TWOW101-1': {
        'id': 'TWOW101-1',
        'title': 'Hosting a Good TWOW',
        'department': department_list['TWOW Design']['name'],
        'professor': professor_list['450096592582737920']['id'],
        'professor_name': professor_list['450096592582737920']['name'],
        'ta': None,
        'description': 'A project-oriented class that covers all aspects of creating a TWOW; this includes good prompts, good aesthetics, good presentation and even good twists. Also covers how to avoid bad prompts, bad aesthetics, bad presentation and bad twists.'
    },
    'TWOW101-2': {
        'id': 'TWOW101-2',
        'title': 'Hosting a Good TWOW',
        'department': department_list['TWOW Design']['name'],
        'professor': professor_list['236257776421175296']['id'],
        'professor_name': professor_list['236257776421175296']['name'],
        'ta': None,
        'description': '<i>[NOTE: Due to popular demand, two sections have been opened for this course. You may not sign up for both TWOW101-1 and TWOW101-2.]</i>'
    },
    'ARG403': {
        'id': 'ARG403',
        'title': 'Alternate Reality Games (secret)',
        'department': department_list['Sociology']['name'],
        'professor': professor_list['849279934987894805']['id'],
        'professor_name': professor_list['849279934987894805']['name'],
        'ta': professor_list['236257776421175296']['id'],
        'description': '&nbsp;'
    },
    'ARG404': {
        'id': 'ARG404',
        'title': 'Alternate Reality Games',
        'department': department_list['Sociology']['name'],
        'professor': professor_list['849279934987894805']['id'],
        'professor_name': professor_list['849279934987894805']['name'],
        'ta': professor_list['236257776421175296']['id'],
        'description': '&nbsp;'
    },
    'GEO013': {
        'id': 'GEO013',
        'title': 'Surveying Intermediate Geographical Nuisances: Amateur Litany',
        'department': department_list['Sociology']['name'],
        'professor': professor_list['210285266814894081']['id'],
        'professor_name': professor_list['210285266814894081']['name'],
        'ta': professor_list['212983348325384200']['id'],
        'description': 'An introductory examination of abnormalities in border disputes as a result of political disagreements.<br><br><b>I think saying that, historically, I\'m subpar ontologically, necessitates excessive backlash. I\'m surely, certainly unrivalled in teaching.</b>'
    },
    'ART121': {
        'id': 'ART121',
        'title': 'The Art of Art',
        'department': department_list['Visual Arts']['name'],
        'professor': professor_list['212805953630896128']['id'],
        'professor_name': professor_list['212805953630896128']['name'],
        'ta': None,
        'description': 'DRAW. CREATE. LIBERATE.'
    }
}

### aux ###

def find_link(link_id, links, key='id'):
    for link in links:
        if link[key] == link_id:
            return link
        if link['type'] == 'container':
            link = find_link(link_id, link['link'], key=key)
            if link:
                return link
    return None

def find_container(link_id, links, key='id'):
    for link in links:
        if link[key] == link_id:
            return links
        if link['type'] == 'container':
            container = find_container(link_id, link['link'], key=key)
            if container:
                return container
    return None

def find_containers(links):
    out = []
    for link in links:
        if link['type'] == 'container':
            out += [link] + find_containers(link['link'])
    return out

### checks ###

@jinja_env
def is_professor():
    return discord.authorized and data.get_id() in professor_list

def teaches_class(class_):
    return is_professor() and data.get_id() in (class_['professor'], class_['ta'])

def enrolled_in(class_):
    return discord.authorized and class_['id'] in data.get('classes')

def is_in_purgatory():
    return data.get('purgatory').get('count', 0) > 0

### decorators ###

def requires_valid_class(f):
    #ensures that the specified class id is valid
    @wraps(f)
    def decorator(*args, class_id, **kwargs):
        class_ = class_list.get(class_id)
        if not class_:
            abort(404)
        return f(*args, class_=class_, **kwargs)
    return decorator

def requires_valid_link(f):
    #ensures that the specified link id is valid
    @wraps(f)
    def decorator(*args, class_, link_id, **kwargs):
        link = find_link(link_id, data.get('links', user=class_['id']) or [])
        if not link:
            abort(404)
        return f(*args, class_=class_, link=link, **kwargs)
    return decorator

def requires_submittable_link(f):
    #ensures that the link can be submitted to
    @wraps(f)
    def decorator(*args, class_, link, **kwargs):
        if not link.get('submittable'):
            abort(404)
        return f(*args, class_=class_, link=link, **kwargs)
    return decorator

def requires_valid_submission(f):
    #ensures that the specified submission id is valid
    @wraps(f)
    def decorator(*args, class_, link, submission_id, **kwargs):
        submission = link.get('submissions', {}).get(submission_id)
        if not submission:
            abort(404)
        return f(*args, class_=class_, link=link, submission=submission, **kwargs)
    return decorator

def requires_no_submission(f):
    #ensures that the student has not yet submitted anything
    @wraps(f)
    def decorator(*args, class_, link, **kwargs):
        submission_id = data.get_id()
        submission = link.get('submissions', {}).get(submission_id)
        if submission:
            return redirect(url_for('submission_page', class_id=class_['id'], link_id=link['id'], submission_id=submission_id), 303)
        return f(*args, class_=class_, link=link, **kwargs)
    return decorator

def requires_professor(f):
    #checks whether the user is a professor
    @wraps(f)
    @requires_authorization
    def decorator(*args, **kwargs):
        if not is_professor():
            abort(403)
        return f(*args, **kwargs)
    return decorator

def requires_participant(f):
    #checks whether the user is an accepted student or a professor
    @wraps(f)
    @requires_authorization
    def decorator(*args, **kwargs):
        return (
            f(*args, **kwargs)
            if is_professor()
            else requires_accepted(f)(*args, **kwargs)
        )
    return decorator

def requires_class_member(f):
    #sends purgatory members to purgatory if this class is ARG404
    #checks whether a student is enrolled in or a professor is teaching a class
    @wraps(f)
    @requires_participant
    def decorator(*args, class_, **kwargs):
        if class_['id'] == 'ARG404' and is_in_purgatory():
            return redirect(url_for('purgatory'))
        return (
            f(*args, class_=class_, **kwargs)
            if enrolled_in(class_) else
            must_teach_class(f)(*args, class_=class_, **kwargs)
        )
    return decorator

def must_teach_class(f):
    #checks whether the user is this class's professor or ta
    @wraps(f)
    @requires_participant
    def decorator(*args, class_, **kwargs):
        if not teaches_class(class_):
            abort(403)
        return f(*args, class_=class_, **kwargs)
    return decorator

def must_teach_or_own_submission(f):
    #checks whether the user teaches or owns the submission
    @wraps(f)
    @requires_participant
    def decorator(*args, class_, link, submission, **kwargs):
        return (
                f(*args, class_=class_, link=link, submission=submission, **kwargs)
                if data.get_id() == submission.get('id')
                else must_teach_class(f)(*args, class_=class_, link=link, submission=submission, **kwargs)
        )
    return decorator


### routes ###

@app.route('/classes')
@requires_participant
def classes():
    #gets the list of classes taught if a professor or enrolled if a student
    classes = [class_ for class_ in class_list.values() if teaches_class(class_)] if is_professor() else [class_list[class_] for class_ in data.get('classes')]
    return render_template('classes.html', classes=classes)

@app.route('/classes/<string:class_id>')
@requires_valid_class
@requires_class_member
def class_page(*, class_):
    links = data.get('links', user=class_['id'])
    return render_template('classes/class_page.html', class_=class_, links=links)

###

@app.route('/classes/<string:class_id>/upload', methods=['GET', 'POST'])
@requires_valid_class
@must_teach_class
def upload_link(*, class_):
    return {
        'GET': upload_link_get,
        'POST': upload_link_post
    }[request.method](class_=class_)

def upload_link_get(*, class_, link=None):
    #finds all containers and creates id:name key-value pairs from them
    containers = {container['id']: container['name'] for container in find_containers(data.get('links', user=class_['id']) or []) if not link or container['id'] != link['id']}
    return render_template('classes/class_page/link_upload.html', class_=class_, containers=containers, link=link)

def upload_link_post(*, class_, link=None):
    fields = request.form.to_dict()

    #the container is the array in which to post the link - defaults to the class link list
    links = data.get('links', user=class_['id']) or []
    try:
        container = find_link(fields.pop('container'), links)['link']
    except:
        container = links
    
    #containers use the link field to store children
    if fields.get('type') == 'container':
        fields['link'] = []
    
    if link:
        #containers have special links that need to be preserved
        if link.get('type') == 'container' and fields.get('type') == 'container':
            fields['link'] = link['link']
        #populates any other unset fields
        for field in link:
            #checkboxes don't appear when unchecked - treat an unset checkbox as set to false
            if field == 'submittable':
                continue
            if field not in fields:
                fields[field] = link[field]

    #assigns a random id to the link
    while not 'id' in fields or find_link(fields['id'], links):
        fields['id'] = f'{random.randint(0, 9999999999):010d}'
    
    #updates the database
    container.append(fields)
    data.set('links', links, user=class_['id'])

    return redirect(url_for('link_page', class_id=class_['id'], link_id=fields['id']), 303)

###

@app.route('/classes/<string:class_id>/<string:link_id>', methods=['GET', 'POST'])
@requires_valid_class
@requires_class_member
@requires_valid_link
def link_page(*, class_, link):  
    return {
        'GET': link_page_get,
        'POST': link_page_post
    }[request.method](class_=class_, link=link)

def link_page_get(*, class_, link):
    #reads information from the link data
    students = []
    grades = link.get('grades', {})
    comments = link.get('comments', {})
    submissions = link.get('submissions', {})

    #check if the link is gradeable
    try:
        points = float(link['points'])
    except:
        points = 0

    #whether the link is submittable, gradeable, or a viewable submission exists
    view_submissions = (
        points or
        link.get('submittable') or
        bool(submissions if is_professor() else submissions.get(data.get_id()))
    )

    #adds a student to the student list
    def append_student(student):
        #verifies that the grade is a float
        try:
            grade = grades.get(student)
            float(grade)
        except:
            grade = '-'
        students.append({
                'id': student,
                'submission': submissions.get(student),
                'grade': grade,
                'comment': comments.get(student)
            })

    #professors get a list of students and their submissions and grades; students get their own
    if is_professor():
        for student in data.get('students', user=class_['id']):
            append_student(student)
    else:
        append_student(data.get_id())
    
    return render_template('classes/class_page/link_page.html', class_=class_, link=link, view_submissions=view_submissions, students=students)

@must_teach_class
def link_page_post(*, class_, link):
    #ensures that the link is gradeable
    try:
        points = float(link['points'])
    except:
        points = 0
    if points:
        grades = {}
        comments = {}

        #splits the grades (which must be float-parseable)and comments
        fields = request.form.to_dict()
        for key, value in fields.items():
            if key.startswith('grade-'):
                try:
                    float(value)
                    grades[key[6:]] = value
                except:
                    pass
            elif key.startswith('comment-'):
                comments[key[8:]] = value
                

        #gets a reference to an editable copy
        links = data.get('links', user=class_['id'])
        link = find_link(link['id'], links)

        #updates the database
        link['grades'] = grades
        link['comments'] = comments
        data.set('links', links, user=class_['id'])

    return redirect(url_for('link_page', class_id=class_['id'], link_id=link['id']), 303)

###

@app.route('/classes/<string:class_id>/<string:link_id>/edit', methods=['GET', 'POST'])
@requires_valid_class
@must_teach_class
@requires_valid_link
def link_edit(*, class_, link):
    return {
        'GET': link_edit_get,
        'POST': link_edit_post
    }[request.method](class_=class_, link=link)

def link_edit_get(*, class_, link):
    #find the container of the specified link
    links = data.get('links', user=class_['id'])
    container = find_container(link['id'], links)
    if container != links:
        link['container'] = find_link(container, links, key='link')['id']
    
    return upload_link_get(class_=class_, link=link)


def link_edit_post(*, class_, link):
    #delete and reupload the link
    delete_link(class_id=class_['id'], link_id=link['id'])
    return upload_link_post(class_=class_, link=link)

###

@app.route('/classes/<string:class_id>/<string:link_id>/container')
@requires_valid_class
@requires_class_member
@requires_valid_link
def link_container(*, class_, link):
    #find the container of the specified link
    links = data.get('links', user=class_['id'])
    container = find_container(link['id'], links)

    #redirect to the class page if the container is the class link list
    if container == links:
        return redirect(url_for('class_page', class_id=class_['id']), 303)
    else:
        container = find_link(container, links, key='link')
        return redirect(url_for('link_page', class_id=class_['id'], link_id=container['id']), 303)

@app.route('/classes/<string:class_id>/<string:link_id>/delete')
@requires_valid_class
@must_teach_class
@requires_valid_link
def delete_link(*, class_, link):
    #removes the link from its container
    links = data.get('links', user=class_['id'])
    find_container(link['id'], links).remove(link)
    data.set('links', links, user=class_['id'])

    return redirect(url_for('class_page', class_id=class_['id']), 303)

###

@app.route('/classes/<string:class_id>/<string:link_id>/upload', methods=['GET', 'POST'])
@requires_valid_class
@requires_class_member
@requires_valid_link
@requires_submittable_link
@requires_no_submission
def upload_submission(*, class_, link):
    return {
        'GET': upload_submission_get,
        'POST': upload_submission_post
    }[request.method](class_=class_, link=link)

def upload_submission_get(*, class_, link):
    return render_template('classes/class_page/link_page/submission_upload.html', class_=class_, link=link)

def upload_submission_post(*, class_, link):
    fields = request.form.to_dict()
    fields['id'] = data.get_id()

    #gets a reference to an editable copy
    links = data.get('links', user=class_['id'])
    link = find_link(link['id'], links)
    
    #adds the submission
    submissions = link.get('submissions', {})
    submissions[data.get_id()] = fields
    link['submissions'] = submissions

    #updates the database
    data.set('links', links, user=class_['id'])

    return redirect(url_for('submission_page', class_id=class_['id'], link_id=link['id'], submission_id=fields['id']), 303)

###

@app.route('/classes/<string:class_id>/<string:link_id>/<string:submission_id>', methods=['GET', 'POST'])
@requires_valid_class
@requires_class_member
@requires_valid_link
@requires_valid_submission
@must_teach_or_own_submission
def submission_page(*, class_, link, submission):
    return {
        'GET': submission_page_get,
        'POST': submission_page_post
    }[request.method](class_=class_, link=link, submission=submission)

def submission_page_get(*, class_, link, submission):
    #reads information from the link data
    grades = link.get('grades', {})
    comments = link.get('comments', {})

    #verifies that the grade is a float
    try:
        grade = grades.get(submission['id'])
        float(grade)
    except:
        grade = '-'
    comment = comments.get(submission['id'])

    return render_template('classes/class_page/link_page/submission_page.html', class_=class_, link=link, submission=submission, grade=grade, comment=comment)

@must_teach_class
def submission_page_post(*, class_, link, submission):
    #ensures that the link is gradeable
    try:
        points = float(link['points'])
    except:
        points = 0
    if points:
        grades = link.get('grades', {})
        comments = link.get('comments', {})
        
        #updates the data, ensuring that the grade is float-parseable
        fields = request.form.to_dict()
        try:
            grades[submission['id']] =  fields.get('grade')
            float(grades[submission['id']])
        except:
            grades[submission['id']] = None
        comments[submission['id']] = fields.get('comment')
                
        #gets a reference to an editable copy
        links = data.get('links', user=class_['id'])
        link = find_link(link['id'], links)

        #updates the database
        link['grades'] = grades
        link['comments'] = comments
        data.set('links', links, user=class_['id'])

    return redirect(url_for('submission_page', class_id=class_['id'], link_id=link['id'], submission_id=submission['id']), 303)