export class Proxy {
    hostname: string
    port: string
    username: any
    password: any

    constructor (
        host: string, 
        port: string, 
        username?: string, 
        password?: string
    ) {
        this.hostname = host;
        this.port = port;
        this.username = username;
        this.password = password;
    }
}
