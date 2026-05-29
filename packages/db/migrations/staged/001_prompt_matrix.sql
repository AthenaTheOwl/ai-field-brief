create table if not exists prompt_lenses (
  id text primary key,
  name text not null,
  mode text not null,
  category text not null,
  prompt_path text not null,
  output_schema_path text,
  purpose text not null,
  active boolean not null default true,
  version int not null default 1,
  created_at timestamptz not null default now()
);

create table if not exists matrix_runs (
  id text primary key,
  profile_id text not null,
  lookback_start timestamptz not null,
  lookback_end timestamptz not null,
  status text not null,
  created_at timestamptz not null default now(),
  completed_at timestamptz,
  metadata jsonb not null default '{}'::jsonb
);

create table if not exists matrix_cells (
  id text primary key,
  matrix_run_id text not null references matrix_runs(id),
  source_item_id text not null,
  lens_id text not null references prompt_lenses(id),
  mode text not null,
  content text not null,
  structured jsonb not null default '{}'::jsonb,
  source_refs jsonb not null default '[]'::jsonb,
  confidence text not null,
  faithfulness_status text not null default 'not_checked',
  status text not null default 'created',
  warnings jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  unique(matrix_run_id, source_item_id, lens_id)
);

create index if not exists matrix_cells_source_idx on matrix_cells(source_item_id);
create index if not exists matrix_cells_lens_idx on matrix_cells(lens_id);
create index if not exists matrix_cells_status_idx on matrix_cells(status, faithfulness_status);
