export class Proxy {
    hostname: string
    port: string
    username: any
    password: any

    constructor (host: string, port: string, username: any=null, password: any=null) {
        this.hostname = host;
        this.port = port;
        this.username = username;
        this.password = password;
    }
}
