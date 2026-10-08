<!-- Generated from skills/17-workspace-governance-compliance-engineering/SKILL.md -->
## Chat Membership Privacy & Target-Audience Governance — v1.22.0

### Membership Lists Are Governed Metadata

A list of who belongs to a collaboration space can itself be sensitive organizational information.

Google Chat now supports explicit controls over who can view space membership lists.

Governance should therefore treat:

```text
space membership metadata
```

as a data-access surface, not merely UI decoration.

### Separate Access Policies

Current Chat model separates:

```text
who can discover
who can join
who can view membership
```

An organization's collaboration policy should define these independently where required.

Do not assume discoverability policy should automatically expose member identity.

### Target Audiences

Google Workspace target audiences can define organizational groups permitted to:

- discover spaces;
- join spaces;
- view membership lists.

Document who owns target-audience configuration and who is authorized to apply it to spaces.

### Role-Based Membership Visibility

Membership-list access can also depend on space role.

Governance questions include:

```text
Can ordinary members see the directory?
Only managers?
Managers + assistant managers?
Specified target audiences?
```

Choose deliberately based on business/privacy requirements.

### Restricted Reads Must Not Be Re-exported

If an application or agent has privileged visibility into a membership list:

- do not expose it to a broader audience through dashboards;
- do not cache it in a less-restricted data store;
- do not include it in broad AI context without need.

Authorization on the source API does not automatically govern a copied dataset.

### Audit Policy Changes

Where membership visibility affects regulated/sensitive collaboration spaces, record:

```text
space
previous policy
new policy
actor
time
reason/change ID
```

using available administrative/audit evidence appropriate to the organization.

### Reconciliation Needs Authorization Context

A governance report that counts members must state whether the caller had complete membership visibility.

Do not publish:

```text
member_count = 0
```

as authoritative if the API result was permission-filtered.

Cross-reference Skills 07, 09, 14, and 16.
