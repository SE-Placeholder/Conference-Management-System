const client = axios.create({
    baseURL: 'https://kind-wind-83282.pktriot.net/'
})

const endpoints = {
    login: 'auth/login',
    logout: 'auth/logout',
    register: 'auth/register',
    isAuthenticated: 'auth/is-authenticated',
    changePassword: 'auth/password/change',
    resetPassword: 'auth/password/reset',

    conferences: 'conferences',
    conferenceDetails: 'conferences/<id>',
    joinConference: 'conferences/<id>/join',

    users: 'users',
    userDetails: 'users/<username>',
    userConferences: '/users/conferences',

    papers: 'papers'
}

const pathEncode = (endpoint, ...arguments) =>
    arguments.reduce((path, argument) =>
        path.replace(/<[^>]*>/, argument),
        endpoint)

const api = {
    auth: {
        login: (username, password) =>
            client.post(endpoints.login, {username, password}),
        logout: () =>
            client.post(endpoints.logout),
        register: (username, email, password1, password2) =>
            client.post(endpoints.register, {username, email, password1, password2}),
        isAuthenticated: () =>
            client.get(endpoints.isAuthenticated),    
        changePassword: () =>
            console.error("NOT IMPLEMENTED"),
        resetPassword: email =>
            client.post(endpoints.resetPassword, {email}),
    },
    conferences: {
        list: () =>
            client.get(endpoints.conferences),
        retrieve: id =>
            client.get(pathEncode(endpoints.conferenceDetails, id)),
        create: (title, description, date, location, deadline, fee) =>
            client.post(endpoints.conferences, {title, description, date, location, deadline, fee}),
        join: id =>
            client.post(pathEncode(endpoints.joinConference, id))
    },
    users: {
        list: () =>
            client.get(endpoints.users),
        retrieve: username =>
            client.get(pathEncode(endpoints.userDetails, username)),
        conferences: () =>
            client.get(endpoints.userConferences)

    },
    papers: {
        list: () =>
            client.get(endpoints.papers),
        create: (title, authors, abstract, paper, keywords, topics) => {
            data = new FormData()
            data.append('title', title)
            data.append('author', authors)
            data.append('abstract', abstract)
            data.append('paper', paper)
            data.append('conference', window.selectedConference)
            data.append('keywords', JSON.stringify(keywords))
            data.append('topics', JSON.stringify(topics))
            return client.post(endpoints.papers, data)
        }
    },

}

client.interceptors.request.use(
    config => {
        access_token = window.localStorage.getItem('x-jwt-access-token')
        if (access_token && config.url != endpoints.login && config.url != endpoints.register)
            config.headers['Authorization'] = `Bearer ${access_token}`
        return config
    },
    error => Promise.reject(error)
)

client.interceptors.response.use(
    response => {
        if (response.config.url == endpoints.login || response.config.url == endpoints.register)
            window.localStorage.setItem('x-jwt-access-token', response.data.access_token)

        if (response.config.url == endpoints.logout)
            window.localStorage.removeItem('x-jwt-access-token')

        return response
    },

    error => {
        if (error.response.config.url == endpoints.isAuthenticated && error.response.status == 401) {
            return Promise.resolve({...error.response, data:{...error.response.data, authenticated:false}})
        }
        if (error.response.config.url == endpoints.logout && error.response.status == 401) {
            return Promise.resolve(error.response)
        }

        console.warn('ERROR INTERCEPTED')
        console.log(`${error.response.config.url} ${error.response.status} ${error.response.statusText}`)
        console.log(error.response)
        console.log(error.request)
        console.log(error.config)

        // if (error.response.status == 401)
        //     window.location.href = 'login.html'

        return Promise.reject(error)
    }
)

