var data = `<div class="col-lg-4 col-md-6 wow fadeInUp filtered_data" data-wow-delay="0.1s">
<div class="property-item rounded overflow-hidden">
    <div class="position-relative overflow-hidden">
        <a href=""><img class="img-fluid" src="{{property.property_data.property_image|last}}"
                alt=""></a>
        <div
            class="selling_option bg-primary rounded text-white position-absolute start-0 top-0 m-4 py-1 px-3">
            For {{property.property_data.selling_option}}</div>
        <div
            class="bg-white rounded-top text-primary position-absolute start-0 bottom-0 mx-4 pt-1 px-3">
            {{property.property_data.property_type}}</div>
    </div>
    <div class="p-4 pb-0">
        <h5 class="text-primary mb-3">
            {% if property.property_data.selling_option == "Rent" %}

            {{property.property_data.property_rent_price}}/Month

            {% else %}

            {{property.property_data.property_value}}

            {% endif %}

        </h5>
        <a class="d-block h5 mb-2" href="">{{property.property_data.property_type}}</a>
        <p><i
                class="fa fa-map-marker-alt text-primary me-2"></i>{{property.property_data.property_address}}
        </p>
    </div>
    <div class="d-flex border-top">
        <small class="flex-fill text-center border-end py-2"><i
                class="fa fa-ruler-combined text-primary me-2"></i>{{property.property_data.geography_area}}
            Sqft</small>
        <small class="flex-fill text-center border-end py-2"><i
                class="fa fa-bed text-primary me-2"></i>{{property.property_data.construction_status}}</small>
        <small class="flex-fill text-center py-2"><i
                class="fa fa-bath text-primary me-2"></i>{{property.property_data.property_age}}
            Year old</small>
    </div>
</div>
</div>`