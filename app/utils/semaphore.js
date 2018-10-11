
/**
 * Lock resource identified by id so that only one call to callback
 * happened at one time.
 * 
 * The given callback is executed if the resource is not locked at the time
 * of the call.
 * 
 * @param {string} id 
 * @param {function} cb - callback to be executed
 */
function Semaphore(id, cb) {
    if (!(this instanceof Semaphore)) {
        return new Semaphore(id, cb)
    }

    if (!Semaphore.list) {
        Semaphore.list = []
    }

    if (exists()) return Promise.resolve()

    add()

    return Promise.resolve(cb()).finally(remove)

    function exists () {
        return Semaphore.list.includes(id)
    }

    function add () {
        Semaphore.list.push(id)
    }

    function remove () {
        Semaphore.list = Semaphore.list.filter(item => item !== id)
    }
}

export default Semaphore 