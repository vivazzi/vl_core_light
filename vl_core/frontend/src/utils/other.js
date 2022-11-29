export const get_router_component_name = (router, locale) => {
    let component_name = router.currentRoute.value.name
    if (locale === 'en' && component_name.startsWith('en_')) component_name = component_name.slice(locale.length + 1)

    return component_name
}


export const params_to_object = entries => {
  const result = {}
  for(const [key, value] of entries) result[key] = value;

  return result;
}
