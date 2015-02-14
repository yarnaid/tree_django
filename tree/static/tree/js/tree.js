function build_tree(depth, node_name, show_level) {
    // get nodes from DB
    // var depth = depth || 1;
    var depth = getParameterByName('depth', depth);
    var node_name = getParameterByName('q', node_name);
    var show_level = getParameterByName('show_level', show_level) || 1;
    var ajax_query = 'ajax_get_tree/?';
    if (depth) {
        ajax_query += '&depth=' + depth;
    }
    if (node_name) {
        ajax_query += '&q=' + node_name;
    }
    $('#tree > ul').empty();
    function add_element_to_tree(value) {
        var new_e = document.createElement('li');
        var new_e_ul = document.createElement('ul');
        var del_a = document.createElement('a');
        var edit_a = document.createElement('a');
        $(del_a).addClass('glyphicon glyphicon-trash');
        $(del_a).click(remove_element);
        $(edit_a).addClass('glyphicon glyphicon-pencil');
        new_e.id = value['id'];
        var li_text = value['text'];
        $(edit_a).text(li_text);
        $(edit_a).click(edit_name);
        $(new_e).append(edit_a);
        if (value['level'] <= show_level) {
            $(new_e).append(' [level:' + value['level'] + ']');
        }
        $(new_e).append(del_a);
        $(new_e).append(new_e_ul);
        $(new_e).attr('level', value['level']);
        var parent_id = 'tree';
        if (value['parent'] != '-1') {
            parent_id = value['parent'];
        }
            // add elements to document
            var parent = $('#' + parent_id + '> ul');
            parent.append(new_e);
        }

        $.getJSON(ajax_query, function (data) {
            // console.profile('build_tree');
            data['nodes'].forEach(add_element_to_tree);
            // async.each(data['nodes'], add_element_to_tree);
            // console.profileEnd();
            $('span#title-badge').text(data['nodes'].length);
        });
    }

    function edit_name () {
        var element = $(this);
        var id = element.parent().attr('id');
        var currnet_name = element.text();
        var new_name = prompt('Please, enter new name of element with id=' + id, currnet_name);
        if (new_name) {
            $.getJSON('ajax_update_name/?' + 'id=' + id + '&name=' + new_name, function (data) {
                if (data['res'] === true) {
                    element.text(data['name']);
                } else {
                    alert('Cannot change element name!');
                }
            });
        }
    }

    function remove_element() {
        var parent = $(this).parent();
        var remove_id = parent.attr('id');
        $.getJSON('ajax_remove_subtree/?id=' + remove_id, function(data) {
            alert('Removed ' + data['res'] + ' element[s]');
            parent.remove();
        });
    }

    function getParameterByName(name, dflt) {
        dflt = dflt || '';
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
        return results === null ? dflt : decodeURIComponent(results[1].replace(/\+/g, " "));
    }
