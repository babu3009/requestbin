-- Add index for owner_email to improve performance of user-specific bin queries
SET search_path TO requestbin_app;

CREATE INDEX IF NOT EXISTS idx_bins_owner_email ON bins(owner_email);

SELECT 'Index idx_bins_owner_email created successfully!' as status;
