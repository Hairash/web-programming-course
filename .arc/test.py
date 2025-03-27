@app.route('/cases/<username>/<event_id>', methods=['PUT'])
def edit_case(username, event_id):
    new_case = request.data.decode('utf-8')
    if username in users and int(event_id) < len(users[usermane]):
        users[username][int(case_id)] = new_case
        return 'case has been edited'
    else:
        return 'case not found'


'''
users == {
    'Semen': [
        'CS party',
        'Programming session',
    ]
}
'''

<p>{{ username }}</p>