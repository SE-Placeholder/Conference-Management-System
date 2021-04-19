<!-- Script Section -->

/* Menu */
Vue.createApp({
    data() {
        return {
            //TODO: move to data store
            authenticated: false,
            logged_user: ""
        }
    },
    mounted() {
        api.auth.isAuthenticated()
            .then(response => {
                this.authenticated = response.data.authenticated
                this.logged_user = response.data.username
            })
            .catch(error => alert(JSON.stringify(error)))
    },
    methods: {
        logout() {
            api.auth.logout()
                .then(response => window.location.reload())
                .catch(error => alert(JSON.stringify(error)))
        },
        showLogin() {
            document.querySelector('#login-modal').style.display = 'block'
        },
        showAddConference() {
            document.querySelector('#add-conference-modal').style.display = 'block'
        }
    }
})
    .mount('#menu')

/* Login */
Vue.createApp({
    data() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        login() {
            api.auth.login(this.username, this.password)
                .then(response => window.location.reload())
                .catch(error => alert(JSON.stringify(error.response.data)))
        }
    }
})
    .mount('#login-modal')

/* Sign up */
Vue.createApp({
    data() {
        return {
            username: '',
            email: '',
            password1: '',
            password2: ''
        }
    },
    methods: {
        register() {
            api.auth.register(this.username, this.email, this.password1, this.password2)
                .then(response => window.location.reload())
                .catch(error => alert(JSON.stringify(error.response.data)))
        }
    }
})
    .mount('#signup-modal')

/* Submit proposal */
Vue.createApp({
    data() {
        return {
            title: '',
            // author: '',
            abstract: '',
            paper: '',
            keywords_list: [],
            topics_list: [],
            authors_list: []
        }
    },
    methods: {
        submitProposal() {
            api.papers.create({
                title: this.title,
                conference: window.selectedConference,
                topics: [...this.topics_list],
                keywords: [...this.keywords_list],
                abstract: this.abstract,
                paper: this.paper,
                authors: [...this.authors_list]
            })
                .then(response => window.location.reload())
                .catch(error => alert(JSON.stringify(error)))
        },
        abstractUpload() {
            this.abstract = document.querySelector('#upload-abstract').files[0]
        },
        paperUpload() {
            this.paper = document.querySelector('#upload-paper').files[0]
        },
        addTag(event, tag_list) {
            event.preventDefault()
            var val = event.target.value.trim()
            if (val.length > 0) {
                tag_list.push(val)
                event.target.value = ''
            }
        },
        removeTag(index, tag_list) {
            tag_list.splice(index, 1)
        },
        removeLastTag(event, tag_list) {
            if (event.target.value.length === 0) {
                this.removeTag(tag_list.length - 1, tag_list)
            }
        }
    }
})
    .mount('#submit-proposal-modal')

/* Create Conference */
Vue.createApp({
    data() {
        return {
            title: '',
            description: '',
            date: new Date().toISOString().replace(/\..*$/, ''),
            location: '',
            deadline: new Date().toISOString().replace(/\..*$/, ''),
            fee: 0
        }
    },
    methods: {
        createConference() {
            api.conferences.create({
                title: this.title,
                description: this.description,
                date: this.date,
                location: this.location,
                deadline: this.deadline,
                fee: this.fee
            })
                .then(response => window.location.reload())
                .catch(error => alert(JSON.stringify(error)))
        }
    }
})
    .mount('#add-conference-modal')

/* Edit Conference */
editConferenceModal = Vue.createApp({
    data() {
        return {
            id: 0,
            title: '',
            description: '',
            date: new Date().toISOString().replace(/\..*$/, ''),
            location: '',
            deadline: new Date().toISOString().replace(/\..*$/, ''),
            fee: 0,
            steering_committee_list: []
        }
    },
    methods: {
        editConference() {
            console.log(this.steering_committee_list)
            alert('alo')
            api.conferences.update({
                id: this.id,
                title: this.title,
                description: this.description,
                date: this.date,
                location: this.location,
                deadline: this.deadline,
                fee: this.fee
            })
                .then(response => window.location.reload())
                .catch(error => alert(JSON.stringify(error)))
        },
        addTag(event, tag_list) {
            event.preventDefault()
            var val = event.target.value.trim()
            if (val.length > 0) {
                tag_list.push(val)
                event.target.value = ''
            }
        },
        removeTag(index, tag_list) {
            tag_list.splice(index, 1)
        },
        removeLastTag(event, tag_list) {
            if (event.target.value.length === 0) {
                this.removeTag(tag_list.length - 1, tag_list)
            }
        }
    }
})
    .mount('#edit-conference-modal')

/* Join Conference */
Vue.createApp({
    data() {
        return {}
    },
    methods: {
        joinConference() {
            api.conferences.join(window.selectedConference)
                .then(response => window.location.reload())
                .catch(error => alert(JSON.stringify(error)))
        }
    }
})
    .mount('#join-conference-modal')

/* Home tab */
Vue.createApp({
    data() {
        return {
            conferences: []
        }
    },
    mounted() {
        api.conferences.list()
            .then(response => this.conferences = response.data)
            .catch(error => console.log(error))
    },
    methods: {
        showSubmissionModal(id) {
            window.selectedConference = id
            document.getElementById('submit-proposal-modal').style.display = 'block'
        },
        showConfirmJoinModal(id, name) {
            window.selectedConference = id
            document.getElementById('join-conference-modal-title').innerText = name
            document.getElementById('join-conference-modal').style.display = 'block'
        }
    }
})
    .mount('#home-tab')

/* Dashboard tab */
Vue.createApp({
    data() {
        return {
            conferences: [],
            papers: []
        }
    },
    mounted() {
        api.user.conferences()
            .then(response => this.conferences = response.data)
            .catch(error => alert(JSON.stringify(error)))
        api.user.papers()
            .then(response => this.papers = response.data)
            .catch(error => alert(JSON.stringify(error)))
    },
    methods: {
        showEditConferenceModal(conference) {
            editConferenceModal.$data.title = conference.title
            editConferenceModal.$data.description = conference.description
            editConferenceModal.$data.location = conference.location
            editConferenceModal.$data.fee = conference.fee
            editConferenceModal.$data.deadline = new Date(Date.parse(conference.deadline)).toISOString().replace(/\..*$/, '')
            editConferenceModal.$data.date = new Date(Date.parse(conference.date)).toISOString().replace(/\..*$/, '')
            editConferenceModal.$data.id = conference.id
            document.querySelector('#edit-conference-modal').style.display = 'block'
        }
    }
})
    .mount('#dashboard-tab')

/* Tabified Navigation Menu Switch*/
function openTab(scopeClass, tabName) {
    document.querySelectorAll(scopeClass).forEach(div => div.style.display = "none")
    document.getElementById(tabName).style.display = "block";
}