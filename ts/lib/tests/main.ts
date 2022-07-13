import { request } from "./axios";
import { print_api } from "./get_api"

var line = function () {
    console.log("------------");
}

var done = function () {
    console.log("Done. ");
}

console.log("Test get_api");
print_api();
done()
line();
console.log("Test axios");
request();
done()
console.log("End. ")