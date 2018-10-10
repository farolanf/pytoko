
export function categoryPathStr (categoryPath) {
    return categoryPath
        ? categoryPath.slice(1)
            .map(item => item.name)
            .join(' / ')
        : ''
}