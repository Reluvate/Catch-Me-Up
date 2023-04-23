DROP TABLE IF EXISTS session;
CREATE TABLE session (
    session_id INTEGER PRIMARY KEY,
    session_name TEXT,
    session_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

DROP TABLE IF EXISTS transcripts;
CREATE TABLE transcripts (
    transcript_id INTEGER PRIMARY KEY,
    session_id INTEGER NOT NULL,
    sentence TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_session
        FOREIGN KEY (session_id)
        REFERENCES session (session_id)
);