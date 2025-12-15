CREATE EXTENSION IF NOT EXISTS pgcrypto;
#
CREATE TABLE locations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL
);

CREATE TABLE cameras (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id uuid REFERENCES locations(id),
  name text,
  rtsp_url text
);

CREATE TABLE people_counts (
  id BIGSERIAL PRIMARY KEY,
  camera_id uuid,
  timestamp timestamptz NOT NULL,
  count integer NOT NULL,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE tokens (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id uuid,
  token_number integer,
  status text DEFAULT 'issued',
  issued_at timestamptz DEFAULT now(),
  predicted_wait_seconds integer
);

CREATE INDEX idx_counts_camera_time 
ON people_counts(camera_id, timestamp);
