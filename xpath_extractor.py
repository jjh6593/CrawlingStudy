# xpath_extractor.py

def get_element_xpath(driver, element):
    script = """
    var getElementXPath = function(element) {
        if (element.id !== '') return 'id("' + element.id + '")';
        if (element === document.body) return element.tagName.toLowerCase();

        var ix = 0;
        var siblings = element.parentNode.childNodes;
        for (var i = 0; i < siblings.length; i++) {
            var sibling = siblings[i];
            if (sibling === element) return getElementXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
        }
    };
    return getElementXPath(arguments[0]);
    """
    return driver.execute_script(script, element)
