# Code Organization

The main authored Python package lives at repository root:

```text
safe_moe_locomotion/
```

Earlier bootstrap versions kept a `02_Code/` directory to mirror the
research-project lifecycle layout used in `/home/tomato/3YP`. The approved
structure removes that numbered directory. New reusable code should go into the
package rather than being scattered as standalone scripts.

Use `scripts/` only for:

- migration notes from external frameworks,
- small wrappers that must preserve upstream layout,
- one-off code-reading notes.
