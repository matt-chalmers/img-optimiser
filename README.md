# img-optimiser
Python image optimisation adapter based on Tinify, with support for files, buffers, and AWS S3

## Status

*Possibly Deprecated?*

Originally this module provided useful s3 support and functioned was designed to follow an easily swappable interface in case we wanted to try another optimisation provider later.

But now the Tinify API has basic s3 support, removing a key benefit of the module... I need to confirm if there's any s3 features still needed that Tinify cannot handle. For instance can they handle the public/private file feature of this module?
