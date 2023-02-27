interface ESDocument {
    _id: string;
    _index: string;
    _score: number;
    _source: object;
    _type: string;
    _ignored: string[];
}

interface ESResult {
    took: number;
    timed_out: boolean;
    _shards: {
        total: number;
        successful: number;
        skipped: number;
        failed: number;
    };
    hits: {
        hits: ESDocument[];
        max_score: number;
        total: {
            value: number;
            relation: string;
        };
    }
}

export class ESDocument extends Object { }

export class ESResult extends Object { }