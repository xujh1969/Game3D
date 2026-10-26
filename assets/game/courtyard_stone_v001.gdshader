shader_type spatial;
uniform sampler2D stone_color : source_color, filter_linear_mipmap_anisotropic, repeat_enable;
uniform sampler2D stone_normal : hint_normal, filter_linear_mipmap_anisotropic, repeat_enable;
varying vec3 world_position;
float hash(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
void vertex() { world_position=(MODEL_MATRIX*vec4(VERTEX,1.0)).xyz; }
void fragment() {
	vec2 p=world_position.xz;
	float tile=hash(floor(vec2(p.x,p.y-12.5)/.60+.5));
	vec3 base=texture(stone_color,UV).rgb;
	float patina=sin(p.x*.83+p.y*.31)*sin(p.y*.53)*.5+.5;
	ALBEDO=base*mix(vec3(.62,.68,.64),vec3(1.08,1.08,1.00),tile)*mix(.85,1.08,patina);
	ROUGHNESS=mix(.79,.95,tile);
	NORMAL_MAP=texture(stone_normal,UV).rgb;
	NORMAL_MAP_DEPTH=.55;
}
