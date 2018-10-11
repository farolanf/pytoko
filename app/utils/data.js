
export function categoryPathStr (categoryPath) {
    return categoryPath
        ? categoryPath.slice(1)
            .map(item => item.name)
            .join(' / ')
        : ''
}

export function prepareAd (ad) {
    ad.title = _.startCase(ad.title)
    ad.desc = ad.desc
        .replace(/^(.)/, (all, m1) => m1.toUpperCase())
        .replace(/\.\s*(.)/g, (all, m1) => '. ' + m1.toUpperCase())
    return ad
}