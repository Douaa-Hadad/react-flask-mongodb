import axios from 'axios'

export const getList = () => {
    return axios
        .get('/api/tasks', {
            headers: { 'Content-type': 'application/json' }
        })
        .then(res => {
            return res.data.map(item => [item.title, item._id])
        })
}

export const addToList = term => {
    return axios.post(
        '/api/task',
        { title: term },
        { headers: { 'Content-type': 'application/json' } }
    )
}

export const deleteItem = id => {
    return axios.delete(`/api/task/${id}`, {
        headers: { 'Content-type': 'application/json' }
    })
}

export const updateItem = (term, id) => {
    return axios.put(
        `/api/task/${id}`,
        { title: term },
        { headers: { 'Content-type': 'application/json' } }
    )
}
