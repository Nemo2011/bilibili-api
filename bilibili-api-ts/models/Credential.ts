export class Credential {

    sessdata: string|null=null;
    bili_jct: string|null=null;
    dedeuserid: string|null=null;

    constructor(sessdata="", bili_jct="", dedeuserid="") {
        this.sessdata = sessdata
        this.bili_jct = bili_jct
        this.dedeuserid = dedeuserid
    }

    raise_for_no_sessdata() {
        if (this.sessdata === "") throw "Credential 类需要 sessdata";
    }
    raise_for_no_bili_jct():void{
        if (this.bili_jct === "") throw "Credential 类需要 bili_jct";
    }
    raise_for_no_dedeuserid(){
        if (this.dedeuserid === "") throw "Credential 类需要 dedeuserid";
    }
    get_cookies(){
        return {
            "SESSDATA": this.sessdata,
            "bili_jct": this.bili_jct,
            "DedeUserID": this.dedeuserid
        }
    }

}