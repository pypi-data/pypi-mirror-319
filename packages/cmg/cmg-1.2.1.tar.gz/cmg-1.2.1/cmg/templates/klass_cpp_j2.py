TEMPLATE = """
#include <stdexcept>
#include "{{klass.to_snake_case()}}.hpp"
{%- for include in klass.get_forward_includes() %}
#include "{{include}}.hpp"
{%- endfor %}

namespace {{schema.namespace}}
{

    /*
    unsigned long {{klass.name}}::getId() const {
        return Identifiable::getId();
    }

    void {{klass.name}}::setId(unsigned long id) {
        Identifiable::setId(id);
    }
    */
    
    {{klass.get_create_ptr_type()}} {{klass.name}}::create({{klass.get_create_arguments()}})
    {
            auto object = std::make_shared<{{klass.name}}>(PrivateConstructor());
{%- for field in klass.init_fields(parents=False) %}
            object->{{field.to_camel_case()}} = {{field.to_camel_case()}};
{%- endfor %}
{%- for field in klass.fields %}
    {%- if field.has_parent() %}
            object->{{field.to_camel_case()}} = {{field.to_camel_case()}} ;
        {%- if field._parent_field.is_list %}
            object->{{field.to_camel_case()}}.lock()->addTo{{field._parent_field.to_camel_case(upper_first=True)}}(object, true);
        {%- else %}
            object->{{field.to_camel_case()}}.lock()->set{{field._parent_field.to_camel_case(upper_first=True)}}(object);
        {%- endif %}
    {%- endif %}
{%- endfor %}
            return object;
    }

    void {{klass.name}}::update(std::map<std::string, std::any> fields)
    {
        for (const auto &[key, value] : fields)
        {
{%- for field in klass.get_updatable_fields() %}
            if (key == "{{field.to_camel_case()}}")
            {
                set{{field.to_camel_case(upper_first=True)}}(std::any_cast<{{field.get_cpp_type(cast=True)}}>(value));
                continue;
            }
{%- endfor %}
            throw std::invalid_argument("Invalid field: " + key);
        }
    }

    void {{klass.name}}::destroy(bool fromParent)
    {
{%- for field in klass.get_ordered_fields() %}
    {%- if field.has_parent() %}

        // Remove from parent field for {{field.to_camel_case()}}
        if (!fromParent && !{{field.to_camel_case()}}.expired())
        {
        {%- if field._parent_field.is_list %}
            {{field.to_camel_case()}}.lock()->removeFrom{{field._parent_field.to_camel_case(upper_first=True)}}(getptr());
        {%- else %}
            {{field.to_camel_case()}}.lock()->set{{field._parent_field.to_camel_case(upper_first=True)}}(nullptr);
        {%- endif %}
        }
    {%- endif %}
{%- endfor %}

{%- for field in klass.get_ordered_fields() %}
    {%- if field.is_child %}

        // Destory child field(s) for {{field.to_camel_case()}}
        {%- if field.is_list %}
        std::vector<std::shared_ptr<{{field._child_klass.name}}>> toDestroy = {};
        for (auto &item : {{field.to_camel_case()}})
        {
            toDestroy.push_back(item);
        }
        for (auto &item : toDestroy)
        {
            item->destroy(true);
        }
        {{field.to_camel_case()}}.clear();
        {{field.to_camel_case()}}.shrink_to_fit();
        {%- else %}
        if ({{field.to_camel_case()}} != nullptr)
        {
            {{field.to_camel_case()}}->destroy(true);
        }
        {{field.to_camel_case()}} = nullptr;
        {%- endif %}
    {%- endif %}
{%- endfor %}
    }

    std::shared_ptr<{{klass.name}}> {{klass.name}}::getptr()
    {
        return shared_from_this();
    }
    
{%- for field in klass.get_ordered_fields() %}
    {%- if field.has_parent() %}
        {% if field.is_list %}
    throw std::runtime_error("Cannot set parent field for list for class {{klass.name}} and field {{field.to_camel_case()}}"); 
        {% else %}
    void {{klass.name}}::set{{field.to_camel_case(upper_first=True)}}({{field.get_cpp_type()}} parent)
    {
        {%- if field._parent_field.is_list %}
        // Remove from current parent
        if (!{{field.to_camel_case()}}.expired())
        {
            {{field.to_camel_case()}}.lock()->removeFrom{{field._parent_field.to_camel_case(upper_first=True)}}(getptr());
            {{field.to_camel_case()}}.reset();
        }

        // Add to new parent
        if (!parent.expired())
        {
            parent.lock()->addTo{{field._parent_field.to_camel_case(upper_first=True)}}(getptr(), true);
            {{field.to_camel_case()}} = parent;
        }
        {%- else %}
        // Remove from current parent
        if (!{{field.to_camel_case()}}.expired())
        {
            {{field.to_camel_case()}}.lock()->set{{field._parent_field.to_camel_case(upper_first=True)}}(nullptr);
            {{field.to_camel_case()}}.reset();
        }

        // Add to new parent
        if (!parent.expired())
        {
            parent.lock()->set{{field._parent_field.to_camel_case(upper_first=True)}}(getptr());
            {{field.to_camel_case()}} = parent;
        }
        {%- endif %}
    }
        {% endif %}
    {%- else %}
        {% if field.is_list %}
            {%- if field._child_field %}
    void {{klass.name}}::addTo{{field.to_camel_case(upper_first=True)}}({{field.get_cpp_type(nolist=True)}} item, bool fromChild)
    {
        if (fromChild)
        {
            {{field.to_camel_case()}}.push_back(item);
        }
        else
        {
            item->set{{field._child_field.to_camel_case(upper_first=True)}}(getptr());
        }
    
    }

    void {{klass.name}}::removeFrom{{field.to_camel_case(upper_first=True)}}({{field.get_cpp_type(nolist=True)}} item, bool fromChild)
    {
        if (fromChild)
        {
            {{field.to_camel_case()}}.erase(std::remove({{field.to_camel_case()}}.begin(), {{field.to_camel_case()}}.end(), item), {{field.to_camel_case()}}.end());
        }
        else
        {
            item->reset{{field._child_field.to_camel_case(upper_first=True)}}();
        }
    
    }
            {%- else %}

    void {{klass.name}}::addTo{{field.to_camel_case(upper_first=True)}}({{field.get_cpp_type(nolist=True)}} item)
    {
        {{field.to_camel_case()}}.push_back(item);
    }

    void {{klass.name}}::removeFrom{{field.to_camel_case(upper_first=True)}}({{field.get_cpp_type(nolist=True)}} item)
    {
        {{field.to_camel_case()}}.erase(std::remove({{field.to_camel_case()}}.begin(), {{field.to_camel_case()}}.end(), item), {{field.to_camel_case()}}.end());
    }
            {%- endif %}
        {% else %}
    void {{klass.name}}::set{{field.to_camel_case(upper_first=True)}}({{field.get_cpp_type()}} {{field.to_camel_case()}})
    {
        this->{{field.to_camel_case()}} = {{field.to_camel_case()}};
    }

        {% endif %}
    {%- endif %}

    {%- if field.has_parent(): %}
    void  {{klass.name}}::reset{{field.to_camel_case(upper_first=True)}}()
    {
        if (!{{field.to_camel_case()}}.expired())
        {
    {%- if field._parent_field.is_list %}
            {{field.to_camel_case()}}.lock()->removeFrom{{field._parent_field.to_camel_case(upper_first=True)}}(getptr(), true);
    {%- else %}
            {{field.to_camel_case()}}.lock()->set{{field._parent_field.to_camel_case(upper_first=True)}}(nullptr);
    {%- endif %}
            {{field.to_camel_case()}}.reset();
        }
    }
    {%- endif %}

    {{field.get_cpp_type()}} {{klass.name}}::get{{field.to_camel_case(upper_first=True)}}()
    {
        return {{field.to_camel_case()}};
    }


{%- endfor %}

    void {{klass.name}}::addToIndex(std::shared_ptr<Index> index)
    {
        index->add(getptr());
{%- for field in klass.get_ordered_fields() %}
    {%- if field.is_child %}

        // Add {{field.to_camel_case()}} to index
        {%- if field.is_list %}
        for (auto &item : {{field.to_camel_case()}})
        {
            item->addToIndex(index);
        }
        {%- else %}
        if ({{field.to_camel_case()}} != nullptr)
        {
            {{field.to_camel_case()}}->addToIndex(index);
        }
        {%- endif %}
    {%- endif %}
{%- endfor %}
    }

    void {{klass.name}}::serializeFields(std::ostream &os)
    {
        // Serialize ID
        os.write(reinterpret_cast<const char *>(&id), sizeof(id));

{%- for field in klass.get_ordered_fields() %}

    {%- if field.name != "id"  %}
        {%- if field.has_parent() %}

        // Serialize {{field.to_camel_case()}}
        unsigned long {{field.to_camel_case()}}Id = {{field.to_camel_case()}}.lock() ? {{field.to_camel_case()}}.lock()->getId() : 0;
        os.write(reinterpret_cast<const char *>(&{{field.to_camel_case()}}Id), sizeof({{field.to_camel_case()}}Id));
        {%- elif field.is_child %}
            {%- if field.is_list %}

        // Serialize {{field.to_camel_case()}}
        size_t {{field.to_camel_case()}}Size = {{field.to_camel_case()}}.size();
        os.write(reinterpret_cast<const char *>(&{{field.to_camel_case()}}Size), sizeof({{field.to_camel_case()}}Size));
        for (const auto &item : {{field.to_camel_case()}})
        {
            item->serializeFields(os);
        }
            {%- else %}

        // Serialize {{field.to_camel_case()}}
        if ({{field.to_camel_case()}} == nullptr)
        {
            unsigned long nullId = 0;
            os.write(reinterpret_cast<const char *>(&nullId), sizeof(nullId));
        }
        else
        {
            unsigned long itemId = {{field.to_camel_case()}}->getId();
            os.write(reinterpret_cast<const char *>(&itemId), sizeof(itemId));
            {{field.to_camel_case()}}->serializeFields(os);
        }
            {%- endif %}
        {%- else %}
            {%- if field.get_cpp_type() == "std::string" %}

        // Serialize {{field.to_camel_case()}}
        size_t {{field.to_camel_case()}}Size = {{field.to_camel_case()}}.size();
        os.write(reinterpret_cast<const char *>(&{{field.to_camel_case()}}Size), sizeof({{field.to_camel_case()}}Size));
        os.write({{field.to_camel_case()}}.c_str(), {{field.to_camel_case()}}.size());
            {%- elif not field.is_reference() %}

        // Serialize {{field.to_camel_case()}}
        os.write(reinterpret_cast<const char *>(&{{field.to_camel_case()}}), sizeof({{field.to_camel_case()}}));
            {%- endif %}
        {%- endif %}
    {%- endif %}
{%- endfor %}
    }

    void {{klass.name}}::serializeReferences(std::ostream &os)
    {
{%- for field in klass.get_ordered_fields() %}
    {%- if field.is_reference() and not field.has_parent() and not field.is_child %}
        // Serialize {{field.to_camel_case()}}
        if ( {{field.to_camel_case()}}.expired() )
        {
            unsigned long nullId = 0;
            os.write(reinterpret_cast<const char *>(&nullId), sizeof(nullId));
        }
        else
        {
            unsigned long {{field.to_camel_case()}}Id = {{field.to_camel_case()}}.lock()->getId();
            os.write(reinterpret_cast<const char *>(&{{field.to_camel_case()}}Id), sizeof({{field.to_camel_case()}}Id));
        }
    {%- elif field.is_child %}
        // Serialize {{field.to_camel_case()}}
        {%- if field.is_list %}
        for (const auto &item : {{field.to_camel_case()}})
        {
            item->serializeReferences(os);
        }
        {%- else %}
        if ({{field.to_camel_case()}} != nullptr)
        {
            {{field.to_camel_case()}}->serializeReferences(os);
        }
        {%- endif %}
    {%- endif %}
{%- endfor %}
    }

    std::shared_ptr<{{klass.name}}> {{klass.name}}::deserializeFields(std::istream &is, std::shared_ptr<Index> index)
    {
        auto object = std::make_shared<{{klass.name}}>(PrivateConstructor());
        
        // Deserialize ID
        is.read(reinterpret_cast<char *>(&object->id), sizeof(object->id));

        // Add to index
        object->addToIndex(index);

{%- for field in klass.get_ordered_fields() %}
    {%- if field.name != "id"  %}
        {%- if field.has_parent() %}
        
        // Deserialize {{field.to_camel_case()}}
        unsigned long {{field.to_camel_case()}}Id;
        is.read(reinterpret_cast<char *>(&{{field.to_camel_case()}}Id), sizeof({{field.to_camel_case()}}Id));
        object->{{field.to_camel_case()}} = std::dynamic_pointer_cast<{{field.type}}>(index->get({{field.to_camel_case()}}Id));

        {%- elif field.is_child %}
            {%- if field.is_list %}

        // Deserialize {{field.to_camel_case()}}
        size_t {{field.to_camel_case()}}Size;
        is.read(reinterpret_cast<char *>(&{{field.to_camel_case()}}Size), sizeof({{field.to_camel_case()}}Size));
        for (size_t i = 0; i < {{field.to_camel_case()}}Size; i++)
        {
            auto item = {{field._child_klass.name}}::deserializeFields(is, index);
            object->{{field.to_camel_case()}}.push_back(item);
        }
            {%- else %}

        // Deserialize {{field.to_camel_case()}}
        unsigned long {{field.to_camel_case()}}Id;
        is.read(reinterpret_cast<char *>(&{{field.to_camel_case()}}Id), sizeof({{field.to_camel_case()}}Id));
        if ({{field.to_camel_case()}}Id != 0)
        {
            object->{{field.to_camel_case()}} = {{field._child_klass.name}}::deserializeFields(is, index);
        }
            {%- endif %}
        {%- else %}
            {%- if field.get_cpp_type() == "std::string" %}

        // Deserialize {{field.to_camel_case()}}
        size_t {{field.to_camel_case()}}Size;
        is.read(reinterpret_cast<char *>(&{{field.to_camel_case()}}Size), sizeof({{field.to_camel_case()}}Size));
        char *{{field.to_camel_case()}}Buffer = new char[{{field.to_camel_case()}}Size];
        is.read({{field.to_camel_case()}}Buffer, {{field.to_camel_case()}}Size);
        object->{{field.to_camel_case()}} = std::string({{field.to_camel_case()}}Buffer, {{field.to_camel_case()}}Size);
        delete[] {{field.to_camel_case()}}Buffer;
            {%- elif not field.is_reference() %}

        // Deserialize {{field.to_camel_case()}}
        is.read(reinterpret_cast<char *>(&object->{{field.to_camel_case()}}), sizeof(object->{{field.to_camel_case()}}));
            {%- endif %}
        {%- endif %}
    {%- endif %}
{%- endfor %}

        return object;
    }

    void {{klass.name}}::deserializeReferences(std::istream &is, std::shared_ptr<Index> index)
    {
{%- for field in klass.get_ordered_fields() %}
    {%- if field.is_reference() and not field.has_parent() and not field.is_child %}

        // Deserialize {{field.to_camel_case()}}
        unsigned long {{field.to_camel_case()}}Id;
        is.read(reinterpret_cast<char *>(&{{field.to_camel_case()}}Id), sizeof({{field.to_camel_case()}}Id));
        if ({{field.to_camel_case()}}Id != 0)
        {
            {{field.to_camel_case()}} = std::dynamic_pointer_cast<{{field.type}}>(index->get({{field.to_camel_case()}}Id));
        }
    {%- elif field.is_child %}

        // Deserialize {{field.to_camel_case()}}
        {%- if field.is_list %}
        for (auto &item : {{field.to_camel_case()}})
        {
            item->deserializeReferences(is, index);
        }
        {%- else %}
        if ({{field.to_camel_case()}} != nullptr)
        {
            {{field.to_camel_case()}}->deserializeReferences(is, index);
        }
        {%- endif %}
    {%- endif %}
{%- endfor %}
    }
}
"""
