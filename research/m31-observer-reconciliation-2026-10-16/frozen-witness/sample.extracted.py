def sample():
    registry_entries()
    table = process_table()
    groups = inspect_groups(table)
    owned = {row['pid'] for row in table.values() if row['pgid'] in groups}
    changed = True
    while changed:
        count = len(owned)
        owned.update(row['pid'] for row in table.values() if row['ppid'] in owned)
        changed = count != len(owned)
    require(CAPTURE_PID in table and table[os.getpid()]['ppid'] == CAPTURE_PID,
            'Direct capture parent identity')
    observed_auxiliary = {os.getpid(), CAPTURE_PID} | {child.pid for child in HELPERS} \
        | {row['pid'] for row in table.values() if row['observerProbe']}
    rss = sum(table[pid]['rss'] for pid in owned | observed_auxiliary if pid in table)
    report['rssSamples'] += 1
    report['peakObservedOwnedRSSBytes'] = max(report['peakObservedOwnedRSSBytes'], rss)
    require(rss <= RSS_CAP, 'Sampled owned-process RSS cap')
    require(all(table[pid]['pgid'] in groups for pid in owned), 'Unregistered detached descendant')
    return table
