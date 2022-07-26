export declare const SearchData: {
    search: {
        web_search: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                keyword: string;
                page: string;
            };
            comment: string;
        };
        web_search_by_type: {
            url: string;
            method: string;
            verify: boolean;
            params: {
                keyword: string;
                search_type: string;
                page: string;
            };
            comment: string;
        };
        default_search_keyword: {
            url: string;
            method: string;
            verify: boolean;
            comment: string;
        };
        hot_search_keywords: {
            url: string;
            method: string;
            verify: boolean;
            comment: string;
        };
        suggest: {
            url: string;
            method: string;
            verify: boolean;
            comment: string;
        };
    };
};
