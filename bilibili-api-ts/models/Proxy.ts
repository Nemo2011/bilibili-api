export class Proxy {
    hostname: string
    port: string
    username: any
    password: any

    constructor (config: any) {
        var host = config.host;
        var port = config.port;
        var username = config.username;
        var password = config.password;
        this.hostname = host;
        this.port = port;
        this.username = username;
        this.password = password;
    }
}
