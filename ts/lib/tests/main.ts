import { test_request } from "./axios";
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
test_request().then(value => console.log(value));
done()
console.log("End. ")
