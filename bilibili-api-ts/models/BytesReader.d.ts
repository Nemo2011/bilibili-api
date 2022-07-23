/// <reference types="node" />
export declare class BytesReader {
    __stream: Buffer;
    __offset: number;
    constructor({ stream }: {
        stream: Buffer;
    });
    has_end(): boolean;
    double(LE?: boolean): number;
    float(LE?: boolean): number;
    varint(): number;
    byte(): Buffer;
    string(): string;
    bool(): boolean;
    bytes_string(): Buffer;
    set_pos(pos: number): void;
    get_pos(): number;
}
