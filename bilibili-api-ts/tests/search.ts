import { web_search, web_search_by_type, SearchObjectType } from "../search";

export function test_search() {
    web_search({
        keyword: "Warma", 
    }).then(
        function (value) {
            console.log("web_search()");
        }
    );
    web_search_by_type({
        keyword: "Warma", 
        search_type: SearchObjectType.USER, 
        page: 1
    }).then(
        function (value) {
            console.log("web_search_by_type()");
        }
    )
}
