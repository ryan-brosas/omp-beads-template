# Tasks: {bead-id}

## 1. {Phase name}

### 1.1 {Task name}

```yaml
depends_on: []
parallel: false
conflicts_with: []
files: ["{path}"]
estimated_minutes: {minutes}
```

- [ ] {Specific, verifiable step}
- [ ] {Specific, verifiable step}
- [ ] Verify: {How to check this step}

### 1.2 {Task name} {parallel}

```yaml
depends_on: []
parallel: true
conflicts_with: []
files: ["{path}"]
estimated_minutes: {minutes}
```

- [ ] {Step}
- [ ] Verify: {Check}

## 2. {Phase name}

### 2.1 {Task name}

```yaml
depends_on: ["1.1", "1.2"]
parallel: false
files: ["{path}"]
estimated_minutes: {minutes}
```

- [ ] {Step}
- [ ] Verify: {Check}

## N. Verification

### N.1 Full verification

```yaml
depends_on: ["{all previous task IDs}"]
parallel: false
files: []
estimated_minutes: {minutes}
```

- [ ] {End-to-end check}
- [ ] {End-to-end check}
